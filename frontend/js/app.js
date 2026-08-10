const tg = window.Telegram ? window.Telegram.WebApp : null;

if (tg) {
  tg.expand();
  tg.ready();
}

function haptic(style = 'light') {
  if (tg && tg.HapticFeedback) {
    tg.HapticFeedback.impactOccurred(style);
  }
}

document.getElementById('btn-add-asset').addEventListener('click', () => {
  haptic('medium');
  alert("Varlık ekleme modülü yakında eklenecek!");
});
