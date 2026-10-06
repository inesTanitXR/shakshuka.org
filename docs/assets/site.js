
document.querySelector('.menu-btn')?.addEventListener('click',e=>{const n=document.querySelector('nav.main');const o=n.classList.toggle('open');e.currentTarget.setAttribute('aria-expanded',o)});
document.querySelectorAll('.filters button').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.filters button').forEach(x=>x.classList.remove('on'));b.classList.add('on');const t=b.dataset.t;document.querySelectorAll('.dir .card').forEach(c=>c.classList.toggle('hide',t!=='all'&&c.dataset.t!==t))}));
