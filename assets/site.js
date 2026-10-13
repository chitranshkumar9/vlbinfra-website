// Mobile menu
(function () {
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('site-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
  }
  // Project filters
  var buttons = document.querySelectorAll('.filters button');
  buttons.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.getAttribute('data-filter');
      buttons.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      document.querySelectorAll('.proj').forEach(function (card) {
        card.hidden = !(f === 'all' || card.getAttribute('data-cat') === f);
      });
    });
  });
  // Tap a multi-photo card to see the next photo
  document.querySelectorAll('.ph-next').forEach(function (btn) {
    var list = btn.getAttribute('data-photos').split('|');
    var i = 0, img = btn.querySelector('img'), count = btn.querySelector('span');
    btn.addEventListener('click', function () {
      i = (i + 1) % list.length;
      img.src = list[i];
      count.textContent = (i + 1) + ' / ' + list.length;
    });
  });
  // Enquiry form: compose the message and open WhatsApp or email
  var form = document.getElementById('enquiry-form');
  if (form) {
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var via = (ev.submitter && ev.submitter.getAttribute('data-via')) || 'whatsapp';
      var v = function (id) { return document.getElementById(id).value.trim(); };
      var name = v('enq-name'), org = v('enq-org'), phone = v('enq-phone'), email = v('enq-email'), msg = v('enq-msg');
      var err = document.getElementById('enq-error');
      if (!name || !phone || !msg) { err.hidden = false; return; }
      err.hidden = true;
      var lines = ['Enquiry from vlbinfra.com', '', 'Name: ' + name];
      if (org) lines.push('Organisation: ' + org);
      lines.push('Phone: ' + phone);
      if (email) lines.push('Email: ' + email);
      lines.push('', msg);
      var text = lines.join('\n');
      if (via === 'email') {
        location.href = 'mailto:info@vlbinfra.com?subject=' + encodeURIComponent('Enquiry from ' + name) + '&body=' + encodeURIComponent(text);
      } else {
        window.open('https://wa.me/918077676214?text=' + encodeURIComponent(text), '_blank', 'noopener');
      }
    });
  }
  // Dark / light mode toggle (remembers the choice)
  var tb = document.querySelector('.theme-btn');
  if (tb) {
    var root = document.documentElement;
    var isDark = function () {
      var t = root.getAttribute('data-theme');
      if (t) return t === 'dark';
      return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    };
    var label = function () { tb.setAttribute('aria-label', isDark() ? 'Switch to light mode' : 'Switch to dark mode'); };
    label();
    tb.addEventListener('click', function () {
      var next = isDark() ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('vlb-theme', next); } catch (e) {}
      label();
    });
  }
})();
