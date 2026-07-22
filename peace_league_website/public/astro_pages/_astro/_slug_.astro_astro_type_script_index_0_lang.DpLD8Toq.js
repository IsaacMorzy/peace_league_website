import{a as m,c as g}from"./api.DpwVejkS.js";const l=document.getElementById("category-data").dataset.slug;function s(e){const o=document.createElement("div");return o.textContent=e||"",o.innerHTML.replace(/"/g,"&quot;").replace(/'/g,"&#39;")}function r(e,o){document.getElementById("vote-modal-title").textContent=e,document.getElementById("vote-modal-message").textContent=o,document.getElementById("vote-modal").classList.remove("hidden")}window.closeVoteModal=()=>document.getElementById("vote-modal").classList.add("hidden");async function v(){try{const e=await m(l);if(e.status!=="success")throw new Error(e.message||"Category not found");const{category:o,nominees:a}=e.data;if(document.getElementById("category-name").textContent=o.category_name,document.getElementById("breadcrumb-name").textContent=o.category_name,document.getElementById("category-description").textContent=o.description||"",document.title=`${o.category_name} | Awards`,document.getElementById("nominees-loading").classList.add("hidden"),!a||!a.length){document.getElementById("nominees-empty").classList.remove("hidden");return}document.getElementById("nominee-count").textContent=a.length;const n=document.getElementById("nominees-grid");n.innerHTML=a.map(t=>`
        <div class="card-base p-6" id="nominee-${s(t.name)}">
          <div class="flex gap-6">
            <div class="flex-shrink-0">
              ${t.photo_url?`<img src="${s(t.photo_url)}" alt="${s(t.nominee_name)}" class="w-24 h-24 object-cover rounded-lg bg-surface" />`:'<div class="w-24 h-24 rounded-lg bg-hairline flex items-center justify-center text-steel text-xs">No photo</div>'}
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-start">
                <div>
                  <h3 class="text-heading-5 text-ink mb-1">${s(t.nominee_name)}</h3>
                </div>
                <div class="text-right">
                  <div class="text-2xl font-bold text-ink vote-count" data-votes="${t.votes}">${t.votes.toLocaleString()}</div>
                  <div class="text-xs text-steel uppercase tracking-wide">Votes</div>
                </div>
              </div>
              <p class="text-body-sm text-steel my-4 line-clamp-3">${s(t.description)}</p>
              <div class="mt-auto">
                <button
                  class="btn btn-primary vote-btn"
                  data-nominee-id="${s(t.name)}"
                  data-category-slug="${s(l)}"
                >
                  Vote for this nominee
                </button>
              </div>
            </div>
          </div>
        </div>
      `).join(""),n.querySelectorAll(".vote-btn").forEach(t=>{t.addEventListener("click",()=>u(t))})}catch(e){console.error("Category load error:",e),document.getElementById("nominees-loading").classList.add("hidden"),document.getElementById("nominees-error").classList.remove("hidden")}}async function u(e){const o=e.dataset.nomineeId,a=e.dataset.categorySlug;e.disabled=!0,e.textContent="Submitting…";try{const n=await g(o,a);if(n.status==="success"){const d=e.closest('[id^="nominee-"]').querySelector(".vote-count"),c=parseInt(d.dataset.votes,10)||0;d.dataset.votes=c+1,d.textContent=(c+1).toLocaleString();const i=document.createElement("div");i.className="text-sm text-green-600 font-medium flex items-center gap-2",i.innerHTML='<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg> You voted for this nominee',e.replaceWith(i),r("Vote Confirmed",n.message||"Your vote has been recorded. Thank you for participating.")}else r("Vote Failed",n.message||"Failed to cast vote. Please try again."),e.disabled=!1,e.textContent="Vote for this nominee"}catch(n){console.error("Vote error:",n),r("Error","Network error. Please try again."),e.disabled=!1,e.textContent="Vote for this nominee"}}v();
