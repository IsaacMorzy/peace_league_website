const h=window.ENV?.PUBLIC_API_URL||"";function d(t,o,a,n){const s=performance.now();function r(e){const i=Math.min((e-s)/1500,1),f=1-Math.pow(1-i,3),l=Math.floor(f*o);t.textContent=l===0&&o===0?`${n}0${a}`:`${n}${l.toLocaleString()}${a}`,i<1&&requestAnimationFrame(r)}requestAnimationFrame(r)}const m=new IntersectionObserver(t=>{t.forEach(o=>{if(o.isIntersecting){const a=o.target,n=parseInt(a.dataset.countTarget,10);d(a,n,a.dataset.countSuffix||"",a.dataset.countPrefix||""),m.unobserve(a)}})},{threshold:.4});document.querySelectorAll(".stat-value").forEach(t=>m.observe(t));function p(){document.querySelectorAll(".stat-value").forEach(t=>{const o=parseInt(t.dataset.countTarget,10);o>0&&(t.textContent=`${t.dataset.countPrefix||""}0${t.dataset.countSuffix||""}`,d(t,o,t.dataset.countSuffix||"",t.dataset.countPrefix||""))})}const u=new IntersectionObserver(t=>{t.forEach(o=>{if(o.isIntersecting){const a=o.target,n=parseFloat(a.dataset.progressWidth)||0;requestAnimationFrame(()=>{a.style.width=n+"%"}),u.unobserve(a)}})},{threshold:.3});function g(){document.querySelectorAll(".progress-bar").forEach(t=>u.observe(t))}async function v(){try{const t=await fetch(`${h}/api/method/peace_league_website.api.get_homepage_data`);if(!t.ok)return;const o=await t.json(),a=o.message||o;if(a.status==="success"){const{causes:n,chapters:c,stats:s}=a.data;if(s&&(document.getElementById("stat-donations").dataset.countTarget=s.total_donations||0,document.getElementById("stat-volunteers").dataset.countTarget=s.total_volunteers||0,document.getElementById("stat-chapters").dataset.countTarget=c?.length||0,p()),n&&n.length>0){const r=document.getElementById("causes-container");r.innerHTML=n.slice(0,3).map((e,i)=>`
              <div class="bg-canvas rounded-2xl overflow-hidden border border-hairline shadow-[0_4px_16px_rgba(0,0,0,0.04)] transition-all duration-300 hover:shadow-lg hover:-translate-y-2 animate-in fade-in slide-in-from-bottom-4 duration-700" style="animation-delay: ${i*150}ms">
                ${e.image?`<img src="${e.image}" alt="${e.title}" class="w-full h-48 object-cover"/>`:`<div class="h-48 bg-gradient-to-br from-accent/20 to-accent/5 flex items-center justify-center">
                      <svg class="w-14 h-14 text-accent/30" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
                    </div>`}
                <div class="p-6">
                  <span class="inline-flex items-center px-2 py-0.5 rounded-sm text-xs font-semibold mb-3" style="background-color: rgba(55,114,207,0.15); color: #3772cf;">${e.category||"Cause"}</span>
                  <h3 class="text-xl font-semibold text-ink">${e.title||""}</h3>
                  <p class="mt-2 text-steel line-clamp-3">${e.description||""}</p>
                  ${e.raised_amount>0&&e.goal_amount>0?`
                    <div class="mt-4">
                      <div class="flex justify-between text-sm mb-1.5">
                        <span class="font-medium text-ink">$${e.raised_amount.toLocaleString()}</span>
                        <span class="text-stone">$${e.goal_amount.toLocaleString()}</span>
                      </div>
                      <div class="w-full bg-hairline rounded-full h-2.5 progress-track">
                        <div class="bg-accent h-2.5 rounded-full progress-bar" data-progress-width="${Math.min(e.raised_amount/e.goal_amount*100,100)}" style="width: 0"></div>
                      </div>
                      <p class="mt-1 text-xs text-stone">raised of $${e.goal_amount.toLocaleString()} goal</p>
                    </div>
                  `:""}
                  <a href="/donate?cause=${encodeURIComponent(e.name||"")}" class="mt-4 inline-flex items-center justify-center w-full px-4 py-2.5 bg-primary text-on-dark text-sm font-medium rounded-full hover:bg-charcoal transition-colors">
                    Donate Now
                  </a>
                </div>
              </div>
            `).join(""),g()}}}catch{console.log("API not available, static content shown")}}v();setTimeout(g,500);
