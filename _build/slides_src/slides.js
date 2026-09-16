(function(){
  const slides=[...document.querySelectorAll('.slide')];
  const counter=document.getElementById('counter'), prog=document.getElementById('progress'), notesEl=document.getElementById('notes');
  let i=0;
  function fragsOf(s){return [...s.querySelectorAll('.fragment')];}
  function show(n,allFrags){
    n=Math.max(0,Math.min(slides.length-1,n));
    slides.forEach(s=>s.classList.remove('active'));
    i=n; const s=slides[i]; s.classList.add('active');
    fragsOf(s).forEach(f=>f.classList.toggle('visible',!!allFrags));
    counter.textContent=(i+1)+' / '+slides.length;
    prog.style.width=((i+1)/slides.length*100)+'%';
    const nt=s.querySelector('.notes'); notesEl.innerHTML=nt?nt.innerHTML:'<i>אין הערות לשקף זה</i>';
    location.hash='#'+(i+1);
  }
  function next(){const f=fragsOf(slides[i]).find(x=>!x.classList.contains('visible')); if(f){f.classList.add('visible');return;} show(i+1,false);}
  function prev(){const v=fragsOf(slides[i]).filter(x=>x.classList.contains('visible')); if(v.length){v[v.length-1].classList.remove('visible');return;} show(i-1,true);}
  document.addEventListener('keydown',e=>{
    if(e.target.tagName==='INPUT')return;
    switch(e.key){
      case 'ArrowRight': case ' ': case 'PageDown': case 'Enter': case 'ArrowDown': e.preventDefault(); next(); break;
      case 'ArrowLeft': case 'PageUp': case 'Backspace': case 'ArrowUp': e.preventDefault(); prev(); break;
      case 'Home': show(0,false); break; case 'End': show(slides.length-1,true); break;
      case 'f': case 'F': toggleFS(); break;
      case 'n': case 'N': notesEl.classList.toggle('show'); break;
    }
  });
  function toggleFS(){ if(document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen(); }
  document.getElementById('next').onclick=next; document.getElementById('prev').onclick=prev;
  document.getElementById('fsBtn').onclick=toggleFS; document.getElementById('notesBtn').onclick=()=>notesEl.classList.toggle('show');
  // click on slide: left third = prev, right third = next (works for RTL as "forward = left" too via keys)
  document.getElementById('deck').addEventListener('click',e=>{ if(e.target.closest('a,button'))return; const x=e.clientX/innerWidth; if(x>0.66)next(); else if(x<0.33)prev(); });
  // touch swipe
  let tx=null; addEventListener('touchstart',e=>tx=e.touches[0].clientX); addEventListener('touchend',e=>{ if(tx===null)return; const dx=e.changedTouches[0].clientX-tx; if(Math.abs(dx)>50){ dx<0?next():prev(); } tx=null; });
  const h=parseInt(location.hash.slice(1)); show(isNaN(h)?0:h-1,false);
})();
