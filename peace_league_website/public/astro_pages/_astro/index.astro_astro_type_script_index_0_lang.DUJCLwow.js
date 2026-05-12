const h=window.ENV?.PUBLIC_API_URL||"";function d(t,e,a,n){const s=performance.now();function i(o){const r=Math.min((o-s)/1500,1),g=1-Math.pow(1-r,3),l=Math.floor(g*e);t.textContent=l===0&&e===0?`${n}0${a}`:`${n}${l.toLocaleString()}${a}`,r<1&&requestAnimationFrame(i)}requestAnimationFrame(i)}const u=new IntersectionObserver(t=>{t.forEach(e=>{if(e.isIntersecting){const a=e.target,n=parseInt(a.dataset.countTarget,10);d(a,n,a.dataset.countSuffix||"",a.dataset.countPrefix||""),u.unobserve(a)}})},{threshold:.4});document.querySelectorAll(".stat-value").forEach(t=>u.observe(t));function f(){document.querySelectorAll(".stat-value").forEach(t=>{const e=parseInt(t.dataset.countTarget,10);e>0&&(t.textContent=`${t.dataset.countPrefix||""}0${t.dataset.countSuffix||""}`,d(t,e,t.dataset.countSuffix||"",t.dataset.countPrefix||""))})}const m=new IntersectionObserver(t=>{t.forEach(e=>{if(e.isIntersecting){const a=e.target,n=parseFloat(a.dataset.progressWidth)||0;requestAnimationFrame(()=>{a.style.width=n+"%"}),m.unobserve(a)}})},{threshold:.3});function v(){document.querySelectorAll(".progress-bar").forEach(t=>m.observe(t))}async function p(){try{const t=await fetch(`${h}/api/method/peace_league_website.api.get_homepage_data`);if(!t.ok)return;const e=await t.json(),a=e.message||e;if(a.status==="success"){const{programs:n,chapters:c,stats:s}=a.data;if(s&&(document.getElementById("stat-donations").dataset.countTarget=s.total_donations||0,document.getElementById("stat-volunteers").dataset.countTarget=s.total_volunteers||0,document.getElementById("stat-chapters").dataset.countTarget=c?.length||0,f()),n&&n.length>0){const i=document.getElementById("programs-container");i.innerHTML=n.slice(0,3).map((o,r)=>`
              <div class="bg-canvas rounded-lg overflow-hidden border border-hairline transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:border-accent/30" data-aos="fade-up" data-aos-delay="${r*100}">
                ${o.image?`<img src="${o.image}" alt="${o.title}" class="w-full h-48 object-cover"/>`:'<div class="h-48 bg-hairline"></div>'}
                <div class="p-6">
                  <span class="inline-flex items-center px-2 py-0.5 rounded-sm text-xs font-semibold mb-3" style="background-color: rgba(55,114,207,0.15); color: #3772cf;">${o.category||"Program"}</span>
                  <h3 class="text-xl font-semibold text-ink">${o.title||""}</h3>
                  <p class="mt-2 text-steel line-clamp-3">${o.description||""}</p>
                  ${o.raised_amount>0&&o.goal_amount>0?`
                    <div class="mt-4">
                      <div class="w-full bg-hairline rounded-full h-2 progress-track">
                        <div class="bg-accent h-2 rounded-full progress-bar" data-progress-width="${Math.min(o.raised_amount/o.goal_amount*100,100)}" style="width: 0"></div>
                      </div>
                      <p class="mt-2 text-sm text-stone">$${o.raised_amount.toLocaleString()} raised of $${o.goal_amount.toLocaleString()}</p>
                    </div>
                  `:""}
                </div>
              </div>
            `).join(""),v(),window.AOS&&AOS.refresh()}}}catch{console.log("API not available, using static content"),document.getElementById("programs-container").innerHTML=[{title:"Peace Education Program",category:"Education",description:"Comprehensive peace education workshops for schools and communities, teaching conflict resolution and peaceful communication skills."},{title:"Youth Empowerment Initiative",category:"Youth",description:"Empowering young leaders through mentorship programs, skills training, and community service opportunities in 12 communities."},{title:"Community Reconciliation",category:"Community",description:"Facilitating dialogue and reconciliation processes in communities affected by conflict and division across the Great Lakes region."}].slice(0,3).map(e=>`
          <div class="bg-canvas rounded-lg overflow-hidden border border-hairline transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:border-accent/30">
            <div class="h-48 bg-hairline"></div>
            <div class="p-6">
              <span class="badge-tag">${e.category}</span>
              <h3 class="text-xl font-semibold text-ink mt-2">${e.title}</h3>
              <p class="mt-2 text-steel line-clamp-3">${e.description}</p>
            </div>
          </div>
        `).join("")}}p();
