(function(){
  "use strict";
  const input=document.getElementById("article-search");
  const cards=Array.from(document.querySelectorAll("[data-article]"));
  const counter=document.getElementById("search-count");
  const empty=document.getElementById("search-empty");
  if(!input||!cards.length)return;
  const normalize=s=>(s||"").toLocaleLowerCase().normalize("NFKC").trim();
  function filter(){
    const q=normalize(input.value);
    let count=0;
    cards.forEach(card=>{
      const visible=!q||normalize(card.dataset.search).includes(q);
      card.hidden=!visible;
      if(visible)count++;
    });
    if(counter)counter.textContent=(document.documentElement.lang==="en"?count+" articles":count+" 篇文章");
    if(empty)empty.hidden=count!==0;
  }
  input.addEventListener("input",filter);
  input.addEventListener("search",filter);
  filter();
})();
