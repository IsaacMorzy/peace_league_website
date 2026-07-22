import{b as c}from"./api.DpwVejkS.js";function n(s){const a=document.createElement("div");return a.textContent=s||"",a.innerHTML.replace(/"/g,"&quot;").replace(/'/g,"&#39;")}async function m(){try{const s=await c();if(s.status!=="success")throw new Error(s.message||"API error");const a=s.data,i=document.getElementById("results-container"),r=document.getElementById("results-intro");if(!a.published){r.textContent=a.message||"Results have not been published yet. Check back after December 5, 2026 at 18:00 EAT.",i.innerHTML=`
          <div class="text-center py-16">
            <div class="text-6xl mb-6">🗳️</div>
            <h2 class="text-heading-3 text-ink mb-4">Voting in Progress</h2>
            <p class="text-body-md text-steel max-w-xl mx-auto">
              Results will be announced on <strong>December 5, 2026 at 18:00 EAT</strong>.
              In the meantime, browse categories and cast your vote!
            </p>
            <a href="/awards" class="btn btn-primary mt-6">Browse Categories</a>
          </div>
        `;return}const o=a.results||[];if(r.textContent="Congratulations to all the outstanding nominees and winners! The results were announced on December 5, 2026 at the gala in Nairobi.",!o.length){i.innerHTML='<div class="text-center text-steel py-12">No results available.</div>';return}const l=o.reduce((e,t)=>e+(t.total_votes||0),0),x=o.filter(e=>e.winner).length;i.innerHTML=`
        <div class="mb-8">
          <h2 class="text-heading-3 text-ink mb-2">Winners by Category</h2>
          <p class="text-body-md text-steel">Full ranked results with vote totals. Winners are highlighted with a gold badge.</p>
        </div>
        <div class="space-y-6">
          ${o.map(e=>{if(!e.winner)return`
                <div class="card-base p-6" id="${n(e.slug)}">
                  <div class="mb-4"><h3 class="text-heading-5 text-ink">${n(e.category)}</h3></div>
                  <p class="text-body-sm text-steel">No votes were cast in this category.</p>
                </div>
              `;const t=e.winner,d=t.percentage?t.percentage.toFixed(1):"0.0";return`
              <div class="card-base p-6" id="${n(e.slug)}">
                <div class="mb-4"><h3 class="text-heading-5 text-ink">${n(e.category)}</h3></div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div class="md:col-span-2">
                    <div class="flex gap-5 p-4 bg-accent/5 border-2 border-accent rounded-xl relative">
                      <div class="absolute -top-3 left-4 bg-accent text-white text-xs font-bold px-3 py-1 rounded-full">WINNER</div>
                      ${t.photo?`<img src="${n(t.photo)}" alt="${n(t.name)}" class="w-20 h-20 object-cover rounded-lg flex-shrink-0" />`:'<div class="w-20 h-20 rounded-lg bg-hairline flex items-center justify-center text-steel text-xs flex-shrink-0">No photo</div>'}
                      <div>
                        <h4 class="text-heading-5 text-ink mb-1">${n(t.name)}</h4>
                        <div class="text-sm text-steel">
                          <span class="font-semibold">${(t.votes||0).toLocaleString()}</span> votes
                          <span class="text-hairline mx-2">•</span>
                          <span>${d}% of total</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="flex flex-col justify-center items-center bg-surface rounded-xl p-6">
                    <div class="text-4xl font-bold text-ink mb-2">${(t.votes||0).toLocaleString()}</div>
                    <div class="text-sm text-steel text-center">Votes for winner</div>
                    <div class="mt-4 text-sm text-steel">
                      Total votes: <span class="font-semibold text-ink">${(e.total_votes||0).toLocaleString()}</span>
                    </div>
                  </div>
                </div>
              </div>
            `}).join("")}
        </div>
      `,document.getElementById("summary-stats").classList.remove("hidden"),document.getElementById("sum-categories").textContent=o.length,document.getElementById("sum-votes").textContent=l.toLocaleString()}catch(s){console.error("Results load error:",s),document.getElementById("results-intro").textContent="Unable to load results. Please try again later.",document.getElementById("results-container").innerHTML='<div class="text-center text-brand-error py-12">Failed to load results.</div>'}}m();
