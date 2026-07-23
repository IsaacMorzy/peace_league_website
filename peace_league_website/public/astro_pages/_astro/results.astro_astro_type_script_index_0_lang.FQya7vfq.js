import{b as m}from"./api.qfCwQXoU.js";function s(n){const a=document.createElement("div");return a.textContent=n||"",a.innerHTML.replace(/"/g,"&quot;").replace(/'/g,"&#39;")}async function u(){try{let n=function(e){if(!e.winner)return`
            <div class="card-base p-6" id="${s(e.slug)}">
              <div class="mb-4"><h3 class="text-heading-5 text-ink">${s(e.category)}</h3></div>
              <p class="text-body-sm text-steel">No votes were cast in this category.</p>
            </div>
          `;const t=e.winner,o=t.percentage?t.percentage.toFixed(1):"0.0";return`
          <div class="card-base p-6" id="${s(e.slug)}">
            <div class="mb-4"><h3 class="text-heading-5 text-ink">${s(e.category)}</h3></div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="md:col-span-2">
                <div class="flex gap-5 p-4 bg-accent/5 border-2 border-accent rounded-xl relative">
                  <div class="absolute -top-3 left-4 bg-accent text-[#0a0a0a] text-xs font-bold px-3 py-1 rounded-full">WINNER</div>
                  ${t.photo?`<img src="${s(t.photo)}" alt="${s(t.name)}" class="w-20 h-20 object-cover rounded-lg flex-shrink-0" />`:'<div class="w-20 h-20 rounded-lg bg-hairline flex items-center justify-center text-steel text-xs flex-shrink-0">No photo</div>'}
                  <div>
                    <h4 class="text-heading-5 text-ink mb-1">${s(t.name)}</h4>
                    <div class="text-sm text-steel">
                      <span class="font-semibold">${(t.votes||0).toLocaleString()}</span> votes
                      <span class="text-hairline mx-2">·</span>
                      <span>${o}% of total</span>
                    </div>
                    <div class="mt-3 w-full bg-hairline rounded-full h-2" role="progressbar" aria-valuenow="${Math.round(parseFloat(o))}" aria-valuemin="0" aria-valuemax="100" aria-label="${o}% of votes">
                      <div class="bg-accent h-2 rounded-full transition-all duration-1000 ease-out" style="width: ${o}%"></div>
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
        `};const a=await m();if(a.status!=="success")throw new Error(a.message||"API error");const r=a.data,i=document.getElementById("results-intro");if(!r.published){i.textContent=r.message||"Results have not been published yet. Check back after December 5, 2026 at 18:00 EAT.",container.innerHTML=`
          <div class="text-center py-16">
            <div class="text-6xl mb-6">🗳️</div>
            <h2 class="text-heading-3 text-ink mb-4">Voting in Progress</h2>
            <p class="text-body-md text-steel max-w-xl mx-auto">
              Results will be announced on <strong>December 5, 2026 at 18:00 EAT</strong>.
              In the meantime, browse categories and cast your vote!
            </p>
            <a href="/awards" class="btn btn-primary mt-6">Browse Categories</a>
          </div>
        `;return}const l=r.results||[];if(i.textContent="Congratulations to all the outstanding nominees and winners! The results were announced on December 5, 2026 at the gala in Nairobi.",!l.length){document.getElementById("results-all-content").innerHTML='<div class="text-center text-steel py-12">No results available.</div>',document.getElementById("results-winners-content").innerHTML='<div class="text-center text-steel py-12">No winners yet.</div>';return}const c=l.reduce((e,t)=>e+(t.total_votes||0),0),d=l.filter(e=>e.winner);document.getElementById("results-all-content").innerHTML=l.map(n).join(""),document.getElementById("results-winners-content").innerHTML=d.length?d.map(n).join(""):'<div class="text-center text-steel py-8">All categories have recorded votes.</div>',document.getElementById("summary-stats").classList.remove("hidden"),document.getElementById("sum-categories").textContent=l.length,document.getElementById("sum-votes").textContent=c.toLocaleString()}catch(n){console.error("Results load error:",n),document.getElementById("results-intro").textContent="Unable to load results. Please try again later.",document.getElementById("results-all-content").innerHTML='<div class="text-center text-brand-error py-12">Failed to load results.</div>'}}u();
