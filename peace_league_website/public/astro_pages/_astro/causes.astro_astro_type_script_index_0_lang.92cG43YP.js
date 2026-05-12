const l=window.ENV?.PUBLIC_API_URL||"",c={"peace-education":"https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=600&q=80&auto=format&fit=crop","youth-empowerment":"https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=80&auto=format&fit=crop","community-reconciliation":"https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=600&q=80&auto=format&fit=crop",health:"https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&q=80&auto=format&fit=crop",water:"https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=600&q=80&auto=format&fit=crop",agriculture:"https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=600&q=80&auto=format&fit=crop",training:"https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=600&q=80&auto=format&fit=crop",event:"https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=600&q=80&auto=format&fit=crop"},i=new IntersectionObserver(a=>{a.forEach(o=>{if(o.isIntersecting){const e=o.target,s=parseFloat(e.dataset.progressWidth)||0;requestAnimationFrame(()=>{e.style.width=s+"%"}),i.unobserve(e)}})},{threshold:.3});function d(){document.querySelectorAll(".progress-bar").forEach(a=>i.observe(a))}async function m(){try{const a=await fetch(`${l}/api/method/peace_league_website.api.get_causes`);if(!a.ok)return;const o=await a.json(),e=o.message||o;if(e.status==="success"&&e.data&&e.data.length>0){const s=document.getElementById("causes-list");s.innerHTML=e.data.map((t,r)=>{const n=t.image||c[t.name?.toLowerCase()]||"";return`
            <div class="bg-canvas rounded-2xl border border-hairline overflow-hidden shadow-[0_4px_16px_rgba(0,0,0,0.04)] transition-all duration-300 hover:shadow-lg hover:-translate-y-2 animate-in fade-in slide-in-from-bottom-4 duration-700 img-zoom" style="animation-delay: ${r*100}ms">
              ${n?`<div class="h-48 relative overflow-hidden">
                    <img src="${n}" alt="${t.title}" class="w-full h-full object-cover" loading="lazy" />
                    <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                    <div class="absolute inset-0 flex items-center justify-center">
                      <svg class="w-14 h-14 text-white/30" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
                    </div>
                  </div>`:`<div class="h-48 bg-gradient-to-br from-accent/20 to-accent/5 flex items-center justify-center">
                    <svg class="w-14 h-14 text-accent/30" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
                  </div>`}
              <div class="p-6">
                <span class="badge-tag mb-3">${t.category||"Cause"}</span>
                <h3 class="text-xl font-semibold text-ink">${t.title||""}</h3>
                <p class="mt-2 text-steel line-clamp-3">${t.description||""}</p>
                ${t.start_date?`<p class="mt-4 text-sm text-stone"><span class="font-medium text-ink">Starts:</span> ${new Date(t.start_date).toLocaleDateString()}</p>`:""}
                ${t.raised_amount>0&&t.goal_amount>0?`
                  <div class="mt-4">
                    <div class="flex justify-between text-sm mb-1.5">
                      <span class="font-medium text-ink">$${t.raised_amount.toLocaleString()}</span>
                      <span class="text-stone">$${t.goal_amount.toLocaleString()}</span>
                    </div>
                    <div class="w-full bg-hairline rounded-full h-2.5 progress-track">
                      <div class="bg-accent-deep h-2.5 rounded-full progress-bar" data-progress-width="${Math.min(t.raised_amount/t.goal_amount*100,100)}" style="width: 0"></div>
                    </div>
                    <p class="mt-1 text-xs text-stone">raised of $${t.goal_amount.toLocaleString()} goal</p>
                  </div>
                `:""}
                <a href="/donate?cause=${encodeURIComponent(t.name||"")}" class="mt-4 inline-flex items-center justify-center w-full px-4 py-2.5 bg-primary text-on-dark text-sm font-medium rounded-full hover:bg-charcoal transition-colors">
                  Donate Now
                </a>
              </div>
            </div>`}).join(""),d()}}catch{console.log("API not available, using static content")}}m();
