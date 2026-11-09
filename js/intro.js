/* Primex — intro video splash (home page only).
   Plays assets/videos/intro.mp4 (centred, edges feathered into a backdrop that is
   colour-matched to the video). When it ends the screen splits and slides open to
   both sides, revealing the website. Shows once per browser session
   (add ?intro=1 to the URL to force it). If the video is missing or can't play,
   the site simply opens. */
(function () {
  'use strict';
  var root = document.documentElement;
  if (!root.classList.contains('intro-on')) return;

  var intro = document.getElementById('intro');
  var v = document.getElementById('introVideo');
  if (!intro || !v) { root.classList.remove('intro-on'); return; }

  var skipBtn = intro.querySelector('.intro-skip');
  var playing = false, finished = false, timer;
  var top = null, bot = null;                       // sampled backdrop colours [r,g,b]
  var FEATHER = 0.12;                               // keep in sync with --intro-feather

  function rgb(c) { return 'rgb(' + c[0] + ',' + c[1] + ',' + c[2] + ')'; }

  function cleanup() {
    clearTimeout(timer);
    try { v.pause(); v.removeAttribute('src'); v.load(); } catch (e) {}
    window.removeEventListener('resize', fit);
    window.removeEventListener('orientationchange', fit);
    root.classList.remove('intro-on');
    if (intro.parentNode) intro.parentNode.removeChild(intro);
  }

  /* average colour of the video's top and bottom edge -> vertical gradient backdrop */
  function sampleEdges() {
    var w = 48, h = 27, c = document.createElement('canvas');
    c.width = w; c.height = h;
    var x = c.getContext('2d');
    x.drawImage(v, 0, 0, w, h);
    function avg(y0, y1) {
      var d = x.getImageData(0, y0, w, y1 - y0).data, r = 0, g = 0, b = 0, n = d.length / 4;
      for (var i = 0; i < d.length; i += 4) { r += d[i]; g += d[i + 1]; b += d[i + 2]; }
      return [Math.round(r / n), Math.round(g / n), Math.round(b / n)];
    }
    top = avg(0, 2); bot = avg(h - 2, h);
  }

  /* size the video: CSS gives the width (--intro-w), here we also keep it inside
     ~86% of the screen height so it never overflows on landscape phones / short windows */
  function fit() {
    if (finished || !v.videoWidth) return;
    v.style.width = ''; v.style.height = 'auto';
    var r = v.getBoundingClientRect(), maxH = window.innerHeight * 0.86;
    if (r.height > maxH) v.style.width = Math.floor(maxH * v.videoWidth / v.videoHeight) + 'px';
    paintBackdrop();
  }

  function paintBackdrop() {
    if (!top || finished) return;
    var r = v.getBoundingClientRect();
    intro.style.background = 'linear-gradient(to bottom,' + rgb(top) + ' 0,' + rgb(top) + ' ' + r.top + 'px,' +
      rgb(bot) + ' ' + r.bottom + 'px,' + rgb(bot) + ' 100%)';
  }

  function onFirstFrame() {
    try { sampleEdges(); } catch (e) { /* file:// taints canvas -> keep CSS fallback */ }
    fit();                                            // sizes the video, then paints the backdrop
  }

  /* video missing / blocked / skipped before it started: just fade out */
  function quick(why) {
    if (finished) return; finished = true;
    if (/[?&]intro/.test(location.search)) {          // ?intro=1 -> show the reason on screen
      var m = document.createElement('div');
      m.style.cssText = 'position:absolute;left:0;right:0;top:40%;text-align:center;color:#fff;font:600 16px/1.6 system-ui,sans-serif;padding:0 24px';
      m.innerHTML = 'Intro video problem:<br>' + (typeof why === 'string' ? why : 'video could not play') +
        '<br><small style="font-weight:400;opacity:.8">Expected file: ' + v.getAttribute('data-src') + '</small>';
      intro.appendChild(m);
      return;                                          // stay here so the message can be read (Skip closes it)
    }
    if (window.console) console.warn('[intro] skipped:', (typeof why === 'string' ? why : 'video could not play') + ' -> check assets/videos/intro.mp4');
    intro.classList.add('fade');
    setTimeout(cleanup, 480);
  }

  /* feathered copy of the current video frame, same box as on screen */
  function featheredFrame(rect, dpr) {
    var t = document.createElement('canvas');
    t.width = Math.max(1, Math.round(rect.width * dpr)); t.height = Math.max(1, Math.round(rect.height * dpr));
    var x = t.getContext('2d');
    x.drawImage(v, 0, 0, t.width, t.height);
    x.globalCompositeOperation = 'destination-in';
    function mask(horizontal) {
      var g = horizontal ? x.createLinearGradient(0, 0, t.width, 0) : x.createLinearGradient(0, 0, 0, t.height);
      g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(FEATHER, 'rgba(0,0,0,1)');
      g.addColorStop(1 - FEATHER, 'rgba(0,0,0,1)'); g.addColorStop(1, 'rgba(0,0,0,0)');
      x.fillStyle = g; x.fillRect(0, 0, t.width, t.height);
    }
    mask(true); mask(false);
    return t;
  }

  /* normal ending: freeze last frame into two halves, slide them apart */
  function open() {
    if (finished) return; finished = true;
    clearTimeout(timer);
    try {
      if (!v.videoWidth) throw new Error('no frame');
      var W = intro.clientWidth, H = intro.clientHeight;
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var r = v.getBoundingClientRect();

      var c1 = document.createElement('canvas');
      c1.width = Math.round(W * dpr); c1.height = Math.round(H * dpr);
      var ctx = c1.getContext('2d');
      var bg = ctx.createLinearGradient(0, 0, 0, c1.height);
      var t = top || [111, 112, 116], b = bot || t;
      var y0 = Math.min(1, Math.max(0, r.top / H)), y1 = Math.min(1, Math.max(0, r.bottom / H));
      bg.addColorStop(0, rgb(t)); bg.addColorStop(y0, rgb(t)); bg.addColorStop(y1, rgb(b)); bg.addColorStop(1, rgb(b));
      ctx.fillStyle = bg; ctx.fillRect(0, 0, c1.width, c1.height);
      ctx.drawImage(featheredFrame(r, dpr), Math.round(r.left * dpr), Math.round(r.top * dpr));

      var c2 = document.createElement('canvas');
      c2.width = c1.width; c2.height = c1.height;
      c2.getContext('2d').drawImage(c1, 0, 0);

      intro.querySelector('.intro-left').appendChild(c1);
      intro.querySelector('.intro-right').appendChild(c2);
    } catch (e) {
      finished = false; quick('could not freeze last frame'); return;   // soft-fade fallback
    }
    intro.classList.add('split');
    intro.style.background = 'transparent';
    void intro.offsetWidth;                              // flush layout so the slide animates
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { intro.classList.add('open'); });
    });
    setTimeout(cleanup, 1200);
  }

  v.muted = true; v.defaultMuted = true; v.playsInline = true;
  v.addEventListener('loadeddata', onFirstFrame);
  v.addEventListener('playing', function () {
    playing = true; clearTimeout(timer);
    try { sessionStorage.setItem('primexIntro', '1'); } catch (e) {}
  });
  v.addEventListener('ended', function () { setTimeout(open, 250); });
  v.addEventListener('error', function () { quick('video file not found or format not supported'); });
  v.addEventListener('loadedmetadata', fit);
  window.addEventListener('resize', fit);
  window.addEventListener('orientationchange', fit);

  if (skipBtn) skipBtn.addEventListener('click', function () { if (finished) cleanup(); else if (playing) open(); else quick('skipped'); });
  document.addEventListener('keydown', function (e) {
    if (!finished && e.key === 'Escape') { playing ? open() : quick('skipped'); }
  });

  v.src = v.getAttribute('data-src');
  var p = v.play();
  if (p && p.catch) p.catch(function () { quick('autoplay blocked'); });

  /* safety net: video never starts within 6s -> open the site */
  timer = setTimeout(function () { if (!playing) quick('video did not start in 6s'); }, 6000);
})();