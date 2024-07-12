// const signIn = document.querySelector('#signin-btn');
// const signInForm = document.querySelector('#signin');

// signIn.addEventListener('click', ()=>{
//   signInForm.classList.add("active")
// })


// document.addEventListener('click', (event) => {
//   if (!signInForm.contains(event.target) && !signIn.contains(event.target)) {
//     signInForm.classList.remove('active');
//   }
// });




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
const loginBtn = document.getElementById('signin-btn');

loginBtn.addEventListener('click', () => {
  fetch('/login')
   .then(response => response.text())
   .then(html => {
      document.getElementById('modal-universal').classList.add('active');
      document.getElementById('modal-universal').innerHTML = html;
      
    });
});