(function(){var h={autoOpenDelay:3e4,proactiveDelay:15e3},t={department:null,user:null,context:null,conversationHistory:[],leadCaptured:!1,appointmentRequested:!1,surveySent:!1,messagesSent:0,startTime:Date.now(),lastTopic:null};try{var g=localStorage.getItem("pleague-user");g&&(t.user=JSON.parse(g));var f=localStorage.getItem("pleague-chat-state");f&&Object.assign(t,JSON.parse(f))}catch{}var d={countries:{Kenya:{cities:["Nairobi","Kisumu","Mombasa","Nakuru"],programs:["All programs"]},Uganda:{cities:["Kampala","Gulu","Mbale"],programs:["Peace Education","Youth Mentorship"]},Rwanda:{cities:["Kigali","Butare","Gisenyi"],programs:["Community Reconciliation","Healthcare"]},Tanzania:{cities:["Dar es Salaam","Arusha","Dodoma"],programs:["Peace Education","Clean Water"]},Ethiopia:{cities:["Addis Ababa","Bahir Dar","Hawassa"],programs:["Peace Education","Healthcare"]},DRC:{cities:["Kinshasa","Lubumbashi","Goma"],programs:["Community Reconciliation","Emergency Relief"]},"South Sudan":{cities:["Juba","Wau","Malakal"],programs:["Emergency Relief","Peace Education"]},Somalia:{cities:["Mogadishu","Hargeisa","Garowe"],programs:["Healthcare","Emergency Relief"]},Burundi:{cities:["Bujumbura","Gitega"],programs:["Community Reconciliation","Youth Mentorship"]},Mozambique:{cities:["Maputo","Beira","Nampula"],programs:["Clean Water","Healthcare"]},Madagascar:{cities:["Antananarivo","Toamasina"],programs:["Peace Education","Women Empowerment"]},Malawi:{cities:["Lilongwe","Blantyre"],programs:["Clean Water","Healthcare"]}},programs:[{name:"Peace Education",description:"Teaching conflict resolution and peace-building skills in schools across Africa.",impact:"45+ schools, 10,000+ students, 500+ teachers trained",how:"We train teachers, provide curriculum, facilitate student peace clubs, and organize inter-school peace dialogues.",cost:"$50 trains one teacher, $500 trains a whole school staff",countries:["Kenya","Uganda","Rwanda","Tanzania","Ethiopia","South Sudan"]},{name:"Youth Mentorship",description:"Empowering young leaders with skills to build peace in their communities.",impact:"1,200+ volunteers, 10,000+ youth reached",how:"We pair young Africans with trained mentors for 12-month programs focusing on leadership, conflict resolution, and community service.",cost:"$25/month sponsors one youth for a year",countries:["Kenya","Uganda","Rwanda","Tanzania","Ethiopia","DRC"]},{name:"Community Reconciliation",description:"Bringing divided communities together through dialogue and understanding.",impact:"200+ communities reconciled, 15,000+ participants",how:"We facilitate community dialogues, mediate conflicts, and build local peace committees.",cost:"$200 runs a one-day community reconciliation workshop",countries:["DRC","South Sudan","Burundi","Rwanda","Somalia"]},{name:"Healthcare Outreach",description:"Providing medical services to remote and conflict-affected areas.",impact:"50,000+ people served, 200+ health workers trained",how:"We organize medical camps, provide health education, train community health workers, and supply essential medicines.",cost:"$100 provides healthcare for 10 people for a month",countries:["Somalia","South Sudan","DRC","Mozambique","Malawi"]},{name:"Clean Water Projects",description:"Building water wells and sanitation facilities in underserved communities.",impact:"100+ wells built, 30,000+ people with clean water access",how:"We drill wells, install water purification systems, build latrines, and train communities in water management.",cost:"$500 drills a well serving 200+ people",countries:["Kenya","Tanzania","Mozambique","Malawi","Madagascar"]},{name:"Women Empowerment",description:"Supporting women as peacebuilders and leaders in their communities.",impact:"5,000+ women empowered, 1,000+ microloans disbursed",how:"We provide microfinance, vocational training, leadership development, and support women's peace committees.",cost:"$25 provides a microloan to a woman entrepreneur",countries:["Kenya","Uganda","Rwanda","Tanzania","Ethiopia"]}],donations:{impact:[{amount:"$25",impact:"Provides clean water for a family for one month"},{amount:"$50",impact:"Trains one peace teacher"},{amount:"$100",impact:"Provides healthcare for 10 people for a month"},{amount:"$200",impact:"Runs a one-day community reconciliation workshop"},{amount:"$500",impact:"Drills a well serving 200+ people"},{amount:"$1,000",impact:"Launches a youth mentorship program in one community"}]}},W={donate:"I'd love to help you make a difference! You can donate via M-Pesa, credit card, bank transfer, or PayPal at peaceleagueafrica.org/donate. Every dollar counts — $50 trains a peace teacher, $25 provides clean water for a family. Would you like to know more about how your donation will be used?",volunteer:"We'd love to have you join our team of 1,200+ volunteers! Visit peaceleagueafrica.org/volunteer to apply. We have roles in teaching, healthcare, communications, IT, and more. What skills or interests do you have? I can help find the perfect match.",partner:"We're always looking for partners who share our vision of peace! We work with NGOs, governments, corporations, and community organizations. Visit peaceleagueafrica.org/partner or email partner@peaceleagueafrica.org. What type of partnership are you interested in?",events:"We have exciting events coming up! The HWPL Interfaith Dialogue is on May 30 in Nairobi, followed by the Peace Education Summit on June 15. Check out peaceleagueafrica.org/events for the full calendar. Would you like to register for any of these?",countries:"We operate in 12 African countries: Kenya, Uganda, Rwanda, Tanzania, Ethiopia, DRC, South Sudan, Somalia, Burundi, Mozambique, Madagascar, and Malawi. Each country has tailored programs addressing local peace-building needs. Which country are you interested in?",mission:"Peace League Africa was founded in 2015 with a simple belief: every community deserves peace. We transform conflict into hope through education, mentorship, and reconciliation. In 10 years, we've reached 50,000+ lives across 12 countries. Would you like to know about our specific programs?",contact:`You can reach us at:
📧 info@peaceleagueafrica.org
📞 +254 700 000 000
📍 Kenda House, Tom Mboya Street, Nairobi, Kenya

Our team typically responds within 24 hours during business hours (Mon-Fri, 8am-6pm EAT).`,programs:`We have 6 core programs:
📚 Peace Education (45+ schools)
👥 Youth Mentorship (1,200+ volunteers)
🤝 Community Reconciliation
🏥 Healthcare Outreach
💧 Clean Water Projects
👩 Women Empowerment

Which program interests you most? I can share more details about how to get involved.`,impact:`Our impact in numbers:
• 45+ schools with peace education
• 12 countries across Africa
• 1,200+ active volunteers
• 50,000+ lives transformed
• 100+ wells built
• 5,000+ women empowered
• 95% of donations go to programs

Would you like to see our latest impact report?`,price:"Most of our events are free or low-cost to ensure accessibility. Special galas and fundraising events may have ticket prices ranging from $25-$100. Would you like me to check the specific event you're interested in?",schedule:"Our events typically run on weekends (Saturday-Sunday). Workshops are 1-2 days, summits 2-3 days, and community events are usually single-day affairs. We also have virtual events throughout the week. When are you available?",age:`Our programs are open to all ages! 🌟
• Youth programs: Ages 12-25
• Community programs: All ages welcome
• Volunteers: 18+ (16+ with parental consent)
• Healthcare outreach: All ages

There's something for everyone at Peace League Africa!`,safety:`Your safety is our top priority. 🛡️
• All events follow local health guidelines
• Field volunteers receive comprehensive safety training
• We provide emergency contacts and 24/7 support
• Insurance coverage for all volunteers
• Cultural sensitivity training

Would you like to know more about safety at a specific event or program?`,mpesa:`To donate via M-Pesa:
1. Go to Lipa na M-Pesa
2. Enter Business Number: 123456
3. Enter Account Number: Your Phone Number
4. Enter Amount: Your donation
5. Enter your M-Pesa PIN
6. Confirm the transaction

You'll receive a confirmation SMS and a tax receipt via email.`,tax:`Yes, all donations are tax-deductible! 🎉
• We're a registered nonprofit in Kenya
• Registration No. OP.218/051/2015-0281/90876
• Receipts are sent automatically via email
• We provide annual donation statements

You can claim these donations on your tax return.`,corporate:`We offer comprehensive corporate partnership packages:
• CSR programs with measurable impact
• Team building volunteer days
• Co-branded events and campaigns
• Employee giving programs
• Annual impact reports
• Tax benefits

Email partner@peaceleagueafrica.org to discuss your organization's goals.`,school:`Our Peace Education program is transformative! 📚
• 45+ schools across 8 countries
• We train teachers in conflict resolution
• Provide peace education curriculum
• Facilitate student peace clubs
• Organize inter-school peace dialogues
• Impact: 10,000+ students reached

Would you like to partner with us to bring peace education to a school near you?`,healthcare:`Our Healthcare Outreach saves lives! 🏥
• Medical camps in remote areas
• Health education programs
• Community health worker training
• Essential medicine distribution
• Emergency response in conflict zones
• Impact: 50,000+ people served

Would you like to support our healthcare programs or volunteer as a health worker?`,water:`Clean water changes everything! 💧
• 100+ wells built across Africa
• Water purification systems
• Sanitation facilities
• Community water management training
• Impact: 30,000+ people with clean water

$500 drills a well serving 200+ people. Would you like to sponsor a well?`,women:`Women are powerful peacebuilders! 👩
• Microfinance programs
• Vocational training
• Leadership development
• Support for women's peace committees
• Impact: 5,000+ women empowered

Would you like to support our Women Empowerment program or learn about volunteer opportunities?`,youth:`Our Youth Mentorship program transforms lives! 👥
• 12-month mentorship program
• Leadership skills training
• Conflict resolution education
• Community service projects
• Impact: 10,000+ youth trained

Would you like to become a mentor or sponsor a youth participant?`,hello:"Hello! 🌍 I'm Peace Bot from Peace League Africa. I'm here to help you learn about our mission to build peace across Africa and find ways you can get involved. How can I assist you today?",thanks:"You're welcome! 💚 Is there anything else I can help you with? I'm here to answer questions about our programs, events, donations, volunteer opportunities, or partnership options.",goodbye:"Thank you for your interest in Peace League Africa! 🌟 Together, we can build a more peaceful world. Have a wonderful day, and remember — every action counts toward peace!",appointment:`I'd be happy to help you schedule a meeting with our team! 📅

To set up an appointment, please provide:
1. Your name
2. Email address
3. Phone number
4. Preferred date and time
5. What you'd like to discuss

Our team typically responds within 24 hours during business hours (Mon-Fri, 8am-6pm EAT).`,lead:`I'd love to stay in touch! 📬

To better assist you, could you share:
• Your name
• Email address
• Organization (optional)
• How can we help?

This will help our team follow up with you personally.`,sponsor:`Sponsoring a child is one of the most impactful ways to help! 🎓

For $25/month ($300/year), you can sponsor a child's education, which includes:
• School fees
• Uniforms and books
• Meals
• Mentorship support

Visit peaceleagueafrica.org/donate to set up monthly giving.`,remote_volunteer:`Yes, we have remote volunteer opportunities! 🌐

Remote roles include:
• Communications and social media
• IT and web development
• Research and data analysis
• Translation and localization
• Grant writing

You can contribute from anywhere in the world. Visit peaceleagueafrica.org/volunteer to apply.`},y={donate:"donate|donation|give|giving|money|fund|mpesa|payment|contribute|financial",volunteer:"volunteer|help|join|contribute|skills|opportunity|service",partner:"partner|partnership|collaborate|corporate|csr|alliance",events:"event|events|attend|register|upcoming|workshop|summit|conference|gathering",countries:"country|countries|where|operate|location|work in",mission:"mission|vision|about|purpose|why|goal|who are you",contact:"contact|email|phone|reach|talk|speak|office|get in touch",programs:"program|programs|what do you do|activities|initiatives|projects",impact:"impact|results|achieve|difference|outcomes|success|stories",price:"price|cost|ticket|fee|how much|expensive|affordable",schedule:"schedule|time|when|duration|how long|date|calendar",age:"age|old|young|children|kids|youth|adults|seniors",safety:"safe|safety|security|health|emergency|risk|danger",mpesa:"mpesa|lipa|m-pesa|mobile money|stk push",tax:"tax|receipt|deductible|deduction|write off|tax benefit",corporate:"corporate|company|business|team building|csr|enterprise",school:"school|schools|education|teacher|curriculum|students|classroom",healthcare:"health|medical|hospital|clinic|doctor|nurse|patient",water:"water|well|wells|clean water|sanitation|hydration|aquifer",women:"women|woman|gender|empowerment|microfinance|entrepreneur",youth:"youth|young|mentor|mentorship|leadership|next generation",appointment:"schedule|meeting|call|appointment|book|talk to someone|speak with|consultation",lead:"contact info|your info|my info|reach me|get in touch|follow up|stay in touch",hello:"hello|hi|hey|good morning|good afternoon|good evening|greetings",thanks:"thank|thanks|appreciate|grateful|blessed",goodbye:"bye|goodbye|see you|take care|cheers|later",sponsor:"sponsor|sponsoring|child|education|monthly|support a child",remote_volunteer:"remote|virtual|online|work from home|anywhere|digital"},w=["speak with a human","complicated","upset","frustrated","legal","complaint","refund","urgent","emergency","audit","financial statement","board member","executive director"];async function I(e){for(var r=e.toLowerCase(),o=null,u=!1,s="general",a=0;a<w.length;a++)if(r.includes(w[a])){u=!0;break}if(!o){for(var n in y)if(new RegExp(y[n],"i").test(r)){o=W[n],n==="donate"?s="fundraising":n==="volunteer"?s="volunteer-coordination":n==="partner"?s="partnerships":n==="events"&&(s="events");break}}return o||(o=u?"I understand you need specialized assistance. Let me connect you with the right team member who can help you better.":"I can help with donations, volunteering, events, partnerships, and general information about Peace League Africa. What would you like to know?"),{response:o,shouldHandoff:u,department:s}}var p={"/donate":{dept:"fundraising",msg:"Hi! 👋 I see you're interested in supporting our mission. I can help you find the perfect way to make a difference — whether it's a one-time gift, monthly sponsorship, or corporate giving. What would you like to know?"},"/volunteer":{dept:"volunteer-coordination",msg:"Welcome, future peacebuilder! 🌍 I can help you find the perfect volunteer opportunity based on your skills and interests. We have roles in teaching, healthcare, communications, and more. What skills do you have?"},"/events":{dept:"events",msg:"Looking for an event to attend? 📅 I can tell you about our upcoming summits, workshops, and community gatherings. Most are free or low-cost. Would you like me to recommend an event based on your interests?"},"/events/":{dept:"events",msg:"I see you're checking out this event! 🎉 I can help with registration, answer questions about the schedule, or tell you what to expect. What would you like to know?"},"/contact":{dept:"general",msg:"How can we help you today? 📞 Our team is ready to assist with donations, volunteering, partnerships, or any questions about our work across Africa."},"/partner":{dept:"partnerships",msg:"Interested in partnering with Peace League Africa? 🤝 I can help you explore collaboration opportunities. We work with NGOs, governments, corporations, and community organizations. What type of partnership are you considering?"},"/causes":{dept:"programs",msg:"Our programs are making a real difference! 🌟 From peace education in 45+ schools to clean water projects serving 30,000+ people, there are many ways to support. Which cause speaks to you?"},"/careers":{dept:"hr",msg:"Looking to join our team? 💼 I can answer questions about open positions, our culture, and what it's like to work at Peace League Africa. What role interests you?"},"/blog":{dept:"communications",msg:"Enjoying our stories? 📝 I can help you subscribe to our newsletter, share articles, or find specific topics. What caught your interest?"},"/about":{dept:"general",msg:"Want to learn more about Peace League Africa? 🌍 I can share our story, mission, impact, and how you can be part of our journey. What would you like to know?"},"/team":{dept:"general",msg:"Our team is passionate about peace! 👥 I can help you connect with the right person for your inquiry. Who would you like to reach?"},"/gallery":{dept:"communications",msg:"Beautiful moments of peace! 📸 Want to see more, share your own photos, or use our images for a project? I can help with that."}},i={events:[],track:function(e,r){this.events.push({event:e,data:r,timestamp:Date.now()}),window.Libredesk&&window.Libredesk.sendMessage&&window.Libredesk.sendMessage({type:"event",event:e,data:r}),localStorage.setItem("pleague-analytics",JSON.stringify(this.events.slice(-50)))},getMetrics:function(){return{totalMessages:t.messagesSent,conversationDuration:Math.round((Date.now()-t.startTime)/1e3),leadCaptured:t.leadCaptured,appointmentRequested:t.appointmentRequested,department:t.department,events:this.events.length,topicsDiscussed:[...new Set(t.conversationHistory.map(e=>e.content.substring(0,50)))]}}};try{var v=localStorage.getItem("pleague-analytics");v&&(i.events=JSON.parse(v))}catch{}var P={en:{greeting:"Hello! I'm Peace Bot. How can I help you today?",fallback:"I can help with donations, volunteering, events, and more."},fr:{greeting:"Bonjour! Je suis Peace Bot. Comment puis-je vous aider aujourd'hui?",fallback:"Je peux aider avec les dons, le bénévolat, les événements et plus encore."},es:{greeting:"¡Hola! Soy Peace Bot. ¿Cómo puedo ayudarte hoy?",fallback:"Puedo ayudar con donaciones, voluntariado, eventos y más."},pt:{greeting:"Olá! Sou o Peace Bot. Como posso ajudá-lo hoje?",fallback:"Posso ajudar com doações, voluntariado, eventos e mais."},de:{greeting:"Hallo! Ich bin Peace Bot. Wie kann ich Ihnen heute helfen?",fallback:"Ich kann bei Spenden, Freiwilligenarbeit, Veranstaltungen und mehr helfen."},it:{greeting:"Ciao! Sono Peace Bot. Come posso aiutarti oggi?",fallback:"Posso aiutare con donazioni, volontariato, eventi e altro."},ar:{greeting:"مرحباً! أنا Peace Bot. كيف يمكنني مساعدتك اليوم؟",fallback:"يمكنني المساعدة في التبرعات والتطوع والفعاليات والمزيد."},zh:{greeting:"你好！我是 Peace Bot。今天我能帮你什么？",fallback:"我可以帮助您了解捐赠、志愿服务、活动等信息。"},ja:{greeting:"こんにちは！Peace Botです。今日はどのようにお手伝いできますか？",fallback:"寄付、ボランティア、イベントなどについてお手伝いできます。"},ko:{greeting:"안녕하세요! Peace Bot입니다. 오늘 무엇을 도와드릴까요?",fallback:"기부, 봉사활동, 이벤트 등에 대해 도움을 드릴 수 있습니다."},hi:{greeting:"नमस्ते! मैं Peace Bot हूँ। आज मैं आपकी कैसे मदद कर सकता हूँ?",fallback:"मैं दान, स्वयंसेवा, कार्यक्रमों और बहुत कुछ में मदद कर सकता हूँ।"},ru:{greeting:"Здравствуйте! Я Peace Bot. Чем я могу помочь вам сегодня?",fallback:"Я могу помочь с пожертвованиями, волонтерством, мероприятиями и многим другим."},sw:{greeting:"Habari! Mimi ni Peace Bot. Nikisaidiaje leo?",fallback:"Ninaweza kusaidia na michango, kujitolea, matukio, na mengi zaidi."},am:{greeting:"ሰላም! እኔ ፒስ ቦት ነኝ. ዛሬ እንዴት ልረዳዎ?",fallback:"በ捐助፣ በ voluntarism፣ በክስተቶች እና በተጨማሪ ነገሮች ልረዳዎ ይችላል።"},rw:{greeting:"Amakuru! Ndi Peace Bot. Nshobora kukugira iki uyu munsi?",fallback:"Nshobora gufasha mu buryo bwo gutanga, gukorerabushake, nibindi."},lg:{greeting:"Nkulamisa! Nze Peace Bot. Njogera n'akiiki lero?",fallback:"Njogera okuyamba ku mpano, okuwumulira, n'ebintu ebirala."},ha:{greeting:"Sannu! Ni Peace Bot. Yaya zan taimaka a yau?",fallback:"Zan iya taimaka da bayar da gudummawa, aikin yi, tarurruwa, da ƙari."},yo:{greeting:"Bawo ni! Mi ni Peace Bot. Bawo ni le mo le ran se?",fallback:"Mo le ran se pẹlu awọn奉献, iṣura, iṣẹlẹ, ati bii bee loke."},ig:{greeting:"Ndewo! Abụ m Peace Bot. Kedu ka m nyere gị aka taa?",fallback:"Enwere m ike inyere gị aka n'ntụgo, ochikwa, mbibi, na ọzọ."}};function L(e){return e.match(/[ሀ-፿]/)?"am":e.match(/[Ѐ-ӿ]/)?"ru":e.match(/[؀-ۿ]/)?"ar":e.match(/[一-鿿]/)?"zh":e.match(/[぀-ゟ゠-ヿ]/)?"ja":e.match(/[가-힯]/)?"ko":e.match(/[ऀ-ॿ]/)?"hi":e.match(/[ñáéíóúü]/i)?"es":e.match(/[àâçéèêëîïôùûüÿœæ]/i)?"fr":e.match(/[äöüß]/i)?"de":e.match(/\b(ndi|nshobora|amakuru)\b/i)?"rw":e.match(/\b(nkulamisa|njogera|kiiki)\b/i)?"lg":e.match(/\b(habari|nikisaidia|pole)\b/i)?"sw":e.match(/\b(sannu|yaya|taimaka)\b/i)?"ha":e.match(/\b(bawo|ranse|isele)\b/i)?"yo":e.match(/\b(ndewo|ochikwa|mbibi)\b/i)?"ig":"en"}function E(e,r){r=r||1e4;var o=Date.now();function u(){window.Libredesk&&window.Libredesk.show?e():Date.now()-o<r&&setTimeout(u,200)}u()}E(function(){var e=window.location.pathname,r=document.getElementById("prechat-form"),o=document.getElementById("pleague-prechat");if(r&&o){let a=function(){!u&&!sessionStorage.getItem("libredesk-prechat-shown")&&(o.classList.remove("hidden"),o.classList.add("flex"),sessionStorage.setItem("libredesk-prechat-shown","1"))};var u=localStorage.getItem("pleague-prechat-done");setTimeout(a,15e3),r.addEventListener("submit",function(n){n.preventDefault();var c=new FormData(r),l=c.get("name"),b=c.get("email"),k=c.get("phone"),S=c.get("country");if(l&&b&&k&&S){var m={name:l,email:b,phone:k,country:S};localStorage.setItem("pleague-user",JSON.stringify(m)),localStorage.setItem("pleague-prechat-done","1"),t.user=m,t.leadCaptured=!0,window.Libredesk.setUser&&window.Libredesk.setUser(m),o.classList.add("hidden"),o.classList.remove("flex"),window.Libredesk.show(),i.track("prechat_completed",m)}}),o.addEventListener("click",function(n){n.target===o&&(o.classList.add("hidden"),o.classList.remove("flex"))})}for(var s in p)if(e===s||e.startsWith(s)){t.department=p[s].dept,sessionStorage.setItem("libredesk-department",t.department),setTimeout(function(){window.Libredesk.sendMessage&&window.Libredesk.sendMessage({type:"proactive",message:p[s].msg})},h.proactiveDelay);break}setTimeout(function(){sessionStorage.getItem("libredesk-dismissed")||window.Libredesk.show()},h.autoOpenDelay),window.Libredesk.onHide(function(){sessionStorage.setItem("libredesk-dismissed","1"),i.track("conversation_end",i.getMetrics())}),document.querySelectorAll('form[id*="booking"], form[id*="reg-"], form[id*="partner"], form[id*="volunteer"], form[id*="contact"]').forEach(function(a){a.addEventListener("submit",function(n){var c=new FormData(a),l={name:c.get("name")||"",email:c.get("email")||"",phone:c.get("phone")||"",company:c.get("organization")||"",department:t.department};(l.name||l.email)&&(window.Libredesk.setUser&&window.Libredesk.setUser(l),localStorage.setItem("pleague-user",JSON.stringify(l)),t.user=l,t.leadCaptured=!0,i.track("user_data_captured",{source:a.id}))})}),t.user&&window.Libredesk.setUser&&window.Libredesk.setUser(t.user),document.querySelectorAll('form[id*="volunteer"]').forEach(function(a){a.addEventListener("submit",function(){setTimeout(function(){i.track("volunteer_signup")},500)})}),document.querySelectorAll('form[id*="contact"]').forEach(function(a){a.addEventListener("submit",function(){setTimeout(function(){i.track("contact_form_submit")},500)})}),document.querySelectorAll('form[id*="booking"], form[id*="reg-"]').forEach(function(a){a.addEventListener("submit",function(){setTimeout(function(){i.track("event_registration")},500)})}),e==="/donate"&&setTimeout(function(){i.track("donate_page_view")},3e3),window.Libredesk.onMessage&&window.Libredesk.onMessage(async function(a){if(a.sender==="user"){t.messagesSent++,t.conversationHistory.push({role:"user",content:a.text}),i.track("user_message",{text:a.text.substring(0,100)});var n=await I(a.text);n.shouldHandoff&&(window.Libredesk.sendMessage&&window.Libredesk.sendMessage({type:"handoff",department:n.department,reason:"User needs human assistance"}),i.track("handoff_triggered",{department:n.department}))}}),window.Libredesk.onUnreadCountChange&&window.Libredesk.onUnreadCountChange(function(a){var n=document.getElementById("chat-unread-badge");n&&(n.textContent=a,n.classList.toggle("hidden",a===0))}),e==="/donate"&&sessionStorage.setItem("libredesk-context","donor"),e==="/volunteer"&&sessionStorage.setItem("libredesk-context","volunteer"),e.startsWith("/events/")&&sessionStorage.setItem("libredesk-context","attendee"),localStorage.setItem("pleague-chat-state",JSON.stringify(t)),window.PLAChat={getState:function(){return t},getAnalytics:function(){return i.getMetrics()},trackEvent:function(a,n){i.track(a,n)},captureLead:function(a){t.leadCaptured=!0,t.user=a,localStorage.setItem("pleague-user",JSON.stringify(a))},requestAppointment:function(a){t.appointmentRequested=!0,i.track("appointment_requested",a)},detectLanguage:L,translate:function(a,n){return P[n]?.greeting||a},getPrograms:function(){return d.programs},getCountries:function(){return d.countries},getDonationImpact:function(){return d.donations.impact}},console.log("Peace Bot initialized with Gemini AI. Use PLAChat to interact.")})})();
