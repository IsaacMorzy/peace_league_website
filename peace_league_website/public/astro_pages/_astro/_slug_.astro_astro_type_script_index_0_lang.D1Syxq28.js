import{h as u,e as v}from"./api.CuXibZx2.js";const l=document.getElementById("category-data").dataset.slug,h="0x4AAAAAAD78WF4dV1InvrN8";let m="",g=!1;{window.onTurnstileLoad=()=>{window.turnstile&&window.turnstile.render("#turnstile-vote-widget",{sitekey:h,callback:o=>{m=o,g=!0}})};const e=document.createElement("script");e.src="https://challenges.cloudflare.com/turnstile/v0/api.js?onload=onTurnstileLoad",e.async=!0,e.defer=!0,document.head.appendChild(e)}function n(e){const o=document.createElement("div");return o.textContent=e||"",o.innerHTML.replace(/"/g,"&quot;").replace(/'/g,"&#39;")}function a(e,o){document.getElementById("vote-modal-title").textContent=e,document.getElementById("vote-modal-message").textContent=o;const s=document.getElementById("hs-vote-modal");s&&window.HSOverlay?window.HSOverlay.open(s):s&&s.classList.remove("hidden")}window.closeVoteModal=()=>{const e=document.getElementById("hs-vote-modal");e&&window.HSOverlay?window.HSOverlay.close(e):e&&e.classList.add("hidden")};async function p(){try{const e=await u(l);if(e.status!=="success")throw new Error(e.message||"Category not found");const{category:o,nominees:s}=e.data;if(document.getElementById("category-name").textContent=o.category_name,document.getElementById("breadcrumb-name").textContent=o.category_name,document.getElementById("category-description").textContent=o.description||"",document.title=`${o.category_name} | Awards`,document.getElementById("nominees-loading").classList.add("hidden"),!s||!s.length){document.getElementById("nominees-empty").classList.remove("hidden");return}document.getElementById("nominee-count").textContent=s.length;const i=document.getElementById("nominees-grid");i.innerHTML=s.map(t=>`
        <div class="card-base p-6" id="nominee-${n(t.name)}">
          <div class="flex gap-6">
            <div class="flex-shrink-0">
              ${t.photo_url?`<img src="${n(t.photo_url)}" alt="${n(t.nominee_name)}" class="w-24 h-24 object-cover rounded-lg bg-surface" />`:'<div class="w-24 h-24 rounded-lg bg-hairline flex items-center justify-center text-steel text-xs">No photo</div>'}
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-start">
                <div>
                  <h3 class="text-heading-5 text-ink mb-1">${n(t.nominee_name)}</h3>
                </div>
                <div class="text-right">
                  <div class="text-2xl font-bold text-ink vote-count" data-votes="${t.votes}">${t.votes.toLocaleString()}</div>
                  <div class="text-xs text-steel uppercase tracking-wide">Votes</div>
                </div>
              </div>
              <!-- Preline Accordion for nominee description -->
              <div class="hs-accordion-group my-4" data-hs-accordion-always-open>
                <div class="hs-accordion" id="hs-accordion-${n(t.name)}">
                  <div id="hs-accordion-body-${n(t.name)}" class="hs-accordion-content hidden w-full overflow-hidden transition-[height] duration-300" role="region">
                    <p class="text-body-sm text-steel">${n(t.description)}</p>
                  </div>
                  ${t.description&&t.description.length>150?`
                    <p class="text-body-sm text-steel line-clamp-3 accordion-preview" id="accordion-preview-${n(t.name)}">${n(t.description)}</p>
                    <button type="button" class="hs-accordion-toggle inline-flex items-center gap-x-1 text-xs font-medium text-accent hover:text-accent-deep mt-2 transition-colors" aria-controls="hs-accordion-body-${n(t.name)}">
                      <span class="accordion-text-more">Read more</span>
                      <span class="hidden accordion-text-less">Show less</span>
                      <svg class="size-3 transition-transform accordion-chevron" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 9-7 7-7-7"/></svg>
                    </button>
                  `:`
                    <p class="text-body-sm text-steel">${n(t.description)}</p>
                  `}
                </div>
              </div>
              <div class="mt-auto">
                <button
                  class="btn btn-primary vote-btn"
                  data-nominee-id="${n(t.name)}"
                  data-category-slug="${n(l)}"
                >
                  Vote for this nominee
                </button>
              </div>
            </div>
          </div>
        </div>
      `).join(""),i.querySelectorAll(".vote-btn").forEach(t=>{t.addEventListener("click",()=>y(t))})}catch(e){console.error("Category load error:",e),document.getElementById("nominees-loading").classList.add("hidden"),document.getElementById("nominees-error").classList.remove("hidden")}}async function y(e){const o=e.dataset.nomineeId,s=e.dataset.categorySlug;if(!g){a("Verification Required","Please complete the security check."),e.disabled=!1,e.textContent="Vote for this nominee";return}e.disabled=!0,e.textContent="Submitting…";try{const i=await v(o,s,null,m);if(i.status==="success"){const d=e.closest('[id^="nominee-"]').querySelector(".vote-count"),c=parseInt(d.dataset.votes,10)||0;d.dataset.votes=c+1,d.textContent=(c+1).toLocaleString();const r=document.createElement("div");r.className="text-sm text-green-600 font-medium flex items-center gap-2",r.innerHTML='<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg> You voted for this nominee',e.replaceWith(r),a("Vote Confirmed",i.message||"Your vote has been recorded. Thank you for participating.")}else a("Vote Failed",i.message||"Failed to cast vote. Please try again."),e.disabled=!1,e.textContent="Vote for this nominee"}catch(i){console.error("Vote error:",i),a("Error","Network error. Please try again."),e.disabled=!1,e.textContent="Vote for this nominee"}}p();
