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
})();
