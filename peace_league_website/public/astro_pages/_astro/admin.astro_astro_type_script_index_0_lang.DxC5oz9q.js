import{d as y,a as b,b as m,g,c as h}from"./api.CuXibZx2.js";let l=[],c=[],f={};document.querySelectorAll("[data-tab]").forEach(t=>{t.addEventListener("click",()=>{const n=t.dataset.tab;document.querySelectorAll("[data-tab]").forEach(a=>{a.classList.remove("border-accent","text-accent"),a.classList.add("border-transparent","text-steel")}),t.classList.remove("border-transparent","text-steel"),t.classList.add("border-accent","text-accent"),document.querySelectorAll(".tab-content").forEach(a=>a.classList.add("hidden")),document.getElementById(`tab-${n}`).classList.remove("hidden"),n==="nominations"&&d(c),n==="votes"&&p(),n==="categories"&&v()})});async function $(){try{const[t,n,a]=await Promise.all([g(),m(),h()]);t.status==="success"&&(l=t.data||[],v(),E()),n.status==="success"&&(c=n.data||[],document.querySelector("[data-tab].border-accent")?.dataset.tab==="nominations"&&d(c)),a.status==="success"&&(f=a.data||{},document.querySelector("[data-tab].border-accent")?.dataset.tab==="votes"&&p())}catch(t){console.error("Admin load error:",t)}}function v(){const t=document.querySelector("#tab-categories tbody");if(t){if(!l.length){t.innerHTML='<tr><td colspan="4" class="py-8 text-center text-steel text-sm">No categories found.</td></tr>';return}t.innerHTML=l.map(n=>`
      <tr class="border-b border-hairline">
        <td class="py-3 text-ink text-sm font-medium">${i(n.category_name)}</td>
        <td class="py-3 text-steel font-mono text-xs">${i(n.slug)}</td>
        <td class="py-3 text-ink text-sm">${n.nominee_count||0}</td>
        <td class="py-3">
          <button class="text-accent hover:underline text-sm" onclick="alert('Edit: Not yet implemented')">Edit</button>
          <button class="text-brand-error hover:underline text-sm ml-3" onclick="alert('Delete: Not yet implemented')">Delete</button>
        </td>
      </tr>
    `).join("")}}function d(t){const n=document.querySelector("#tab-nominations tbody"),a=document.getElementById("nomination-count");if(a&&(a.textContent=t.length),!!n){if(!t.length){n.innerHTML='<tr><td colspan="6" class="py-8 text-center text-steel text-sm">No nominations found matching your filters.</td></tr>';return}n.innerHTML=t.map(e=>{const o=e.status==="Active"?"bg-green-100 text-green-800":e.status==="Pending"?"bg-amber-100 text-amber-800":"bg-steel/10 text-steel";return`
      <tr class="border-b border-hairline">
        <td class="py-3">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-full bg-surface flex items-center justify-center text-xs font-bold text-accent shrink-0 overflow-hidden">
              ${e.photo_url?`<img src="${i(e.photo_url)}" alt="" class="w-full h-full object-cover" />`:`<span>${(e.nominee_name||"?")[0]}</span>`}
            </div>
            <div>
              <div class="text-ink font-medium text-sm">${i(e.nominee_name)}</div>
              <div class="text-steel text-xs">${i(e.category_name||"")}</div>
            </div>
          </div>
        </td>
        <td class="py-3 text-steel text-sm">${e.submission_date?new Date(e.submission_date).toLocaleDateString():"—"}</td>
        <td class="py-3 text-steel text-xs">${i(e.nominator_name||"")}${e.nominator_email?`<br/><span class="text-muted">${i(e.nominator_email)}</span>`:""}</td>
        <td class="py-3"><span class="px-2 py-0.5 text-xs font-medium rounded-full ${o}">${e.status||"Active"}</span></td>
        <td class="py-3">
          <div class="flex gap-2">
            <select class="text-xs border border-hairline rounded px-1.5 py-1 bg-canvas text-ink status-select" data-nominee="${e.name}">
              <option value="Active" ${e.status==="Active"?"selected":""}>Active</option>
              <option value="Pending" ${e.status==="Pending"?"selected":""}>Pending</option>
              <option value="Rejected" ${e.status==="Rejected"?"selected":""}>Rejected</option>
            </select>
            <button class="text-brand-error hover:underline text-xs delete-btn" data-nominee="${e.name}" data-name="${i(e.nominee_name)}">Delete</button>
          </div>
        </td>
      </tr>
    `}).join(""),n.querySelectorAll(".status-select").forEach(e=>{e.addEventListener("change",async function(){try{await y(this.dataset.nominee,{status:this.value})}catch(o){console.error("Status update failed:",o)}})}),n.querySelectorAll(".delete-btn").forEach(e=>{e.addEventListener("click",async function(){if(confirm(`Delete nomination for "${this.dataset.name}"? This cannot be undone.`))try{const o=await b(this.dataset.nominee);o.status==="success"?(c=c.filter(s=>s.name!==this.dataset.nominee),d(c)):alert("Failed to delete: "+(o.message||"Unknown error"))}catch{alert("Failed to delete nomination")}})})}}function E(){const t=document.getElementById("filter-category");t&&(t.innerHTML='<option value="">All Categories</option>'+l.map(n=>`<option value="${i(n.slug)}">${i(n.category_name)}</option>`).join(""))}async function u(){const t=document.getElementById("filter-search")?.value||"",n=document.getElementById("filter-category")?.value||"",a=document.getElementById("filter-status")?.value||"",e={};t&&(e.search=t),n&&(e.category=n),a&&(e.status=a);try{const o=await m(e);o.status==="success"&&(c=o.data||[],d(c))}catch(o){console.error("Filter error:",o)}}function p(){const t=document.querySelector("#vote-stats-grid"),n=document.getElementById("vote-count");if(!t)return;const a=Object.entries(f);if(n&&(n.textContent=a.length),!a.length){t.innerHTML='<p class="col-span-full text-center text-steel text-sm py-8">No vote data available yet.</p>';return}const e={};l.forEach(o=>{e[o.name]=o.category_name}),t.innerHTML=a.map(([o,s])=>{const r=s.total_votes>0?Math.round(s.top_votes/s.total_votes*100):0;return`
      <div class="p-4 border border-hairline rounded-lg hover:border-accent/30 transition-colors">
        <h3 class="font-semibold text-ink text-sm mb-1">${i(e[o]||o)}</h3>
        <div class="text-2xl font-bold text-accent">${s.total_votes}</div>
        <div class="text-xs text-steel">votes</div>
        <div class="mt-2 h-1.5 bg-hairline rounded-full overflow-hidden">
          <div class="h-full bg-accent rounded-full" style="width: ${r}%"></div>
        </div>
        <div class="mt-1 text-xs text-steel truncate">Leading: ${s.top_nominee?s.top_nominee:"—"} (${r}%)</div>
      </div>
    `}).join("")}function i(t){if(!t)return"";const n=document.createElement("div");return n.textContent=t,n.innerHTML}document.getElementById("filter-search")?.addEventListener("input",L(u,300));document.getElementById("filter-category")?.addEventListener("change",u);document.getElementById("filter-status")?.addEventListener("change",u);function L(t,n){let a;return function(...e){clearTimeout(a),a=setTimeout(()=>t.apply(this,e),n)}}document.querySelector(".btn-secondary")?.addEventListener("click",function(){if(!c.length){alert("No data to export.");return}const n=["Name","Category","Email","Phone","Status","Submitted","Nominator"],a=c.map(r=>[r.nominee_name,r.category_name||r.category,r.nominee_email||"",r.nominee_phone||"",r.status,r.submission_date||"",r.nominator_name||""]),e=[n.join(","),...a.map(r=>r.map(x=>`"${(x||"").replace(/"/g,'""')}"`).join(","))].join(`
`),o=new Blob([e],{type:"text/csv"}),s=document.createElement("a");s.href=URL.createObjectURL(o),s.download="awards-nominations.csv",s.click(),URL.revokeObjectURL(s.href)});$();
