const g=window.ENV?.PUBLIC_API_URL||"";function m(t,e,o,n){const s=performance.now();function r(a){const i=Math.min((a-s)/1500,1),c=1-Math.pow(1-i,3),d=Math.floor(c*e);t.textContent=d===0&&e===0?`${n}0${o}`:`${n}${d.toLocaleString()}${o}`,i<1&&requestAnimationFrame(r)}requestAnimationFrame(r)}const u=new IntersectionObserver(t=>{t.forEach(e=>{if(e.isIntersecting){const o=e.target,n=parseInt(o.dataset.countTarget,10);m(o,n,o.dataset.countSuffix||"",o.dataset.countPrefix||""),u.unobserve(o)}})},{threshold:.4});document.querySelectorAll(".stat-value").forEach(t=>u.observe(t));function p(){document.querySelectorAll(".stat-value").forEach(t=>{const e=parseInt(t.dataset.countTarget,10);e>0&&(t.textContent=`${t.dataset.countPrefix||""}0${t.dataset.countSuffix||""}`,m(t,e,t.dataset.countSuffix||"",t.dataset.countPrefix||""))})}const f=new IntersectionObserver(t=>{t.forEach(e=>{if(e.isIntersecting){const o=e.target,n=parseFloat(o.dataset.progressWidth)||0;requestAnimationFrame(()=>{o.style.width=n+"%"}),f.unobserve(o)}})},{threshold:.3});function h(){document.querySelectorAll(".progress-bar").forEach(t=>f.observe(t))}const v={"peace-education":"https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=600&q=80&auto=format&fit=crop","youth-empowerment":"https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=80&auto=format&fit=crop","community-reconciliation":"https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=600&q=80&auto=format&fit=crop",health:"https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&q=80&auto=format&fit=crop",water:"https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=600&q=80&auto=format&fit=crop",agriculture:"https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=600&q=80&auto=format&fit=crop"};async function b(){try{const t=await fetch(`${g}/api/method/peace_league_website.api.get_homepage_data`);if(!t.ok)return;const e=await t.json(),o=e.message||e;if(o.status==="success"){const{causes:n,chapters:l,stats:s}=o.data;if(s&&(document.getElementById("stat-donations").dataset.countTarget=s.total_donations||0,document.getElementById("stat-volunteers").dataset.countTarget=s.total_volunteers||0,document.getElementById("stat-chapters").dataset.countTarget=l?.length||0,p()),n&&n.length>0){const r=document.getElementById("causes-container");r.innerHTML=n.slice(0,3).map((a,i)=>{const c=a.image||v[a.name?.toLowerCase()]||"";return`
              <div class="bg-canvas rounded-2xl overflow-hidden border border-hairline shadow-[0_4px_16px_rgba(0,0,0,0.04)] transition-all duration-300 hover:shadow-lg hover:-translate-y-2 animate-in fade-in slide-in-from-bottom-4 duration-700 img-zoom" style="animation-delay: ${i*150}ms">
                ${c?`<div class="h-48 relative overflow-hidden">
                      <img src="${c}" alt="${a.title}" class="w-full h-full object-cover" loading="lazy" />
                      <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                      <div class="absolute inset-0 flex items-center justify-center">
                        <svg class="w-14 h-14 text-white/30" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
                      </div>
                    </div>`:`<div class="h-48 bg-gradient-to-br from-accent/20 to-accent/5 flex items-center justify-center">
                      <svg class="w-14 h-14 text-accent/30" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
                    </div>`}
                <div class="p-6">
                  <span class="inline-flex items-center px-2 py-0.5 rounded-sm text-xs font-semibold mb-3" style="background-color: rgba(55,114,207,0.15); color: #3772cf;">${a.category||"Cause"}</span>
                  <h3 class="text-xl font-semibold text-ink">${a.title||""}</h3>
                  <p class="mt-2 text-steel line-clamp-3">${a.description||""}</p>
                  ${a.raised_amount>0&&a.goal_amount>0?`
                    <div class="mt-4">
                      <div class="flex justify-between text-sm mb-1.5">
                        <span class="font-medium text-ink">$${a.raised_amount.toLocaleString()}</span>
                        <span class="text-stone">$${a.goal_amount.toLocaleString()}</span>
                      </div>
                      <div class="w-full bg-hairline rounded-full h-2.5 progress-track">
                        <div class="bg-accent h-2.5 rounded-full progress-bar" data-progress-width="${Math.min(a.raised_amount/a.goal_amount*100,100)}" style="width: 0"></div>
                      </div>
                      <p class="mt-1 text-xs text-stone">raised of $${a.goal_amount.toLocaleString()} goal</p>
                    </div>
                  `:""}
                  <a href="/donate?cause=${encodeURIComponent(a.name||"")}" class="mt-4 inline-flex items-center justify-center w-full px-4 py-2.5 bg-primary text-on-dark text-sm font-medium rounded-full hover:bg-charcoal transition-colors">
                    Donate Now
                  </a>
                </div>
              </div>`}).join(""),h()}}}catch{console.log("API not available, static content shown")}}b();setTimeout(h,500);(function(){const t=document.getElementById("hero-parallax-bg");if(!t)return;let e=!1;window.addEventListener("scroll",()=>{e||(requestAnimationFrame(()=>{const o=document.getElementById("hero-section");o&&o.getBoundingClientRect().bottom>0&&(t.style.transform=`translateY(${window.scrollY*.12}px)`),e=!1}),e=!0)},{passive:!0})})();
