


// show or hide sidebar
const menuBtn = document.querySelector('#menu-btn');
// const closeBtn = document.querySelector('#close-btn');
const sidebar = document.querySelector('aside');

menuBtn.addEventListener('click', () => {
  // sidebar.style.display = 'block'
  sidebar.classList.toggle('active')
})

document.addEventListener('click', (event) => {
  if (!sidebar.contains(event.target) && !menuBtn.contains(event.target)) {
    sidebar.classList.remove('active');
  }
});

// CHANGE THEME

// Get the theme button element
const themeBtn = document.querySelector('.theme-btn');

// Check if dark mode preference is stored in session
let isDarkMode = document.body.classList.contains('dark-theme');

// Apply the initial theme based on the stored preference
if (isDarkMode) {
  document.body.classList.add('dark-theme');
  themeBtn.querySelector('span:first-child').classList.add('active');
  themeBtn.querySelector('span:last-child').classList.remove('active');
} else {
  document.body.classList.remove('dark-theme');
  themeBtn.querySelector('span:first-child').classList.remove('active');
  themeBtn.querySelector('span:last-child').classList.add('active');
}

// Add a click event listener to the theme button
themeBtn.addEventListener('click', () => {
  // Toggle the dark theme class on the body element
  document.body.classList.toggle('dark-theme');

  // Toggle the active class on the button's child elements
  themeBtn.querySelector('span:first-child').classList.toggle('active');
  themeBtn.querySelector('span:last-child').classList.toggle('active');

  // Update the theme preference on the server
  fetch('/set_theme', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
      theme: document.body.classList.contains('dark-theme') ? 'dark' : 'light'
    })
  });
});



// Notification panel
const notificationPanel = document.querySelector('#notification-panel');
const notification = document.querySelector('#notifications');

// Add event listener to the notification icon
notification.addEventListener('click', () => {
  notificationPanel.classList.add('active');
});

// Add event listener to the document (window)
document.addEventListener('click', (event) => {
  if (!notificationPanel.contains(event.target) && !notification.contains(event.target)) {
    notificationPanel.classList.remove('active');
  }
});


const tabItemsNoti = document.querySelectorAll('.tab-item-noti');
const tabContentItemsNoti = document.querySelectorAll('.tab-content-item-noti');

// select tab content item
function selectItemNoti(e){
    removeBorderNoti();
    removeShowNoti();
    // add border to current tab
    this.classList.add('tab-border');
    // grab content item from DOM
    const tabContentItem = document.querySelector(`#${this.id}-content-noti`)
    // add show class
    tabContentItem.classList.add('show');
}
function removeBorderNoti(){
    tabItemsNoti.forEach(item => item.classList.remove('tab-border'));
}
function removeShowNoti(){
    tabContentItemsNoti.forEach(item => item.classList.remove('show'));
}

// Listen for tab click
tabItemsNoti.forEach(item => item.addEventListener('click', selectItemNoti));





// session tabs
const sessiontabs = document.querySelectorAll('.session-tab');
// const tabContentItemsNoti = document.querySelectorAll('.tab-content-item-noti');

// select tab content item
function selectSessionTab(e){
    removeBg();
    // removeShowNoti();
    this.classList.add('active');
    // grab content item from DOM
    // const tabContentItem = document.querySelector(`#${this.id}-content-noti`)
    // add show class
    // tabContentItem.classList.add('show');
}
function removeBg(){
    sessiontabs.forEach(item => item.classList.remove('active'));
}
// function remove(){
//     tabContentItemsNoti.forEach(item => item.classList.remove('show'));
// }

// Listen for tab click
sessiontabs.forEach(item => item.addEventListener('click', selectSessionTab));





// /notification card
const notificationCards = document.querySelectorAll('.notification-card');

notificationCards.forEach(card => {
  card.addEventListener('click', () => {
    card.classList.toggle('open');
    card.classList.remove('unread');
    notificationCards.forEach(otherCard => {
      if (otherCard !== card) {
        otherCard.classList.remove('open');
      }
    });
  });
});

// messages

const tabItems = document.querySelectorAll('.tab-item');
const tabContentItems = document.querySelectorAll('.tab-content-item');

// select tab content item
function selectItem(e){
    removeBorder();
    removeShow();
    // add border to current tab
    this.classList.add('tab-border');
    // grab content item from DOM
    const tabContentItem = document.querySelector(`#${this.id}-content`)
    // add show class
    tabContentItem.classList.add('show');
}
function removeBorder(){
    tabItems.forEach(item => item.classList.remove('tab-border'));
}
function removeShow(){
    tabContentItems.forEach(item => item.classList.remove('show'));
}

// Listen for tab click
tabItems.forEach(item => item.addEventListener('click', selectItem));



// message unread and read
const messageCards = document.querySelectorAll('.message-card');

messageCards.forEach((messageCard) => {
  messageCard.addEventListener('click', () => {
    messageCards.forEach((card) => {
      if (card !== messageCard) {
        card.classList.remove('open');
    }
});
    messageCard.classList.remove('unread')
    messageCard.classList.toggle('open');
  });
});










// settings panel
const settingsPanel = document.querySelector('#setting');
const settings = document.querySelector('#settings');

// Add event listener to the settings icon
settings.addEventListener('click', () => {
  settingsPanel.classList.add('active');
});

// Add event listener to the document (window)
document.addEventListener('click', (event) => {
  if (!settingsPanel.contains(event.target) && !settings.contains(event.target)) {
    settingsPanel.classList.remove('active');
  }
});




// modal unniversal
const modal = document.querySelector('#modal-universal')
const bgBlur = document.querySelector('#bg-blur')

document.addEventListener('click', (event) => {
  if (!modal.contains(event.target) ) {
    modal.classList.remove('active');
    bgBlur.classList.remove('active')
  }
});








// modal

const changePasswordBtn = document.getElementById('btn-change-password');



changePasswordBtn.addEventListener('click', () => {
  fetch('/change_password')
   .then(response => response.text())
   .then(html => {
      const modalBody = document.getElementById('modal-body');
      document.getElementById('modal-universal').classList.add('active');
      document.getElementById('bg-blur').classList.add('active');
      
      document.getElementById('modal-universal').innerHTML = html;
    });
});


const editUserBtn = document.getElementById('btn-edit-user');



editUserBtn.addEventListener('click', () => {
  fetch('/edit_user_info')
   .then(response => response.text())
   .then(html => {
      const modalBody = document.getElementById('modal-body');
      document.getElementById('modal-universal').classList.add('active');
      document.getElementById('bg-blur').classList.add('active');
      
      document.getElementById('modal-universal').innerHTML = html;
    });
});


















// resetPasswordBtn.addEventListener('click', () => {
//   fetch('/reset_password_modal')
//    .then(response => response.text())
//    .then(html => {
//       const modalBody = document.getElementById('modal-body');
//       modalBody.innerHTML = html;
//       document.getElementById('modal-title').textContent = 'Reset Password';
//       document.getElementById('modal-universal').classList.add('active');
//     });
// });

