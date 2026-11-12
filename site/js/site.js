(function(){
  const toggle=document.querySelector('.nav-toggle');
  const nav=document.querySelector('.main-nav');
  if(toggle&&nav){
    toggle.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Close navigation':'Open navigation');nav.classList.toggle('is-open',open)});
    nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('is-open');toggle.setAttribute('aria-expanded','false')}));
  }
  const buttons=[...document.querySelectorAll('[data-filter]')];
  if(buttons.length){
    const cards=[...document.querySelectorAll('.filter-card')];
    const valid=new Set(buttons.map(button=>button.dataset.filter));
    const apply=(category,writeHistory)=>{
      const chosen=valid.has(category)?category:'All';
      buttons.forEach(button=>{const active=button.dataset.filter===chosen;button.classList.toggle('active',active);button.setAttribute('aria-pressed',String(active))});
      cards.forEach(card=>{card.hidden=chosen!=='All'&&card.dataset.category!==chosen});
      if(writeHistory){const u=new URL(window.location.href);if(chosen==='All')u.searchParams.delete('category');else u.searchParams.set('category',chosen);history.replaceState({},'',u.pathname+u.search)}
    };
    buttons.forEach(button=>button.addEventListener('click',()=>apply(button.dataset.filter,true)));
    apply(new URLSearchParams(window.location.search).get('category')||'All',false);
  }
  document.querySelectorAll('a[data-etsy]').forEach(a=>a.addEventListener('click',()=>{
    if(typeof window.gtag==='function')window.gtag('event','etsy_outbound',{product_slug:a.dataset.product||'shop',site_location:a.dataset.location||'unknown',link_url:a.href});
  }));
})();
