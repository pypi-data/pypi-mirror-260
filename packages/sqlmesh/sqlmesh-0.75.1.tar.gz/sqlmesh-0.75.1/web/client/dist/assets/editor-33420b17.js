import{ax as v,q as w,X as m,ay as h,s as d,i as I}from"./index-362aabfe.js";import{M as S}from"./file-c1b8e58b.js";const x=new Worker(new URL("/assets/sqlglot-9a0eff74.js",self.location));function L(){return new Worker(new URL("/assets/lineage-f7b7b3e0.js",self.location),{type:"module"})}const[y,b]=v("tabs"),{tabs:l=[],id:c}=y()??{},f=p(),u=T(f),M=new Map(l.length>0&&w(c)?[]:[[f,u]]),C=m((a,n)=>({storedTabs:l,storedTabId:c,tab:u,tabs:M,engine:x,dialects:[],previewQuery:void 0,previewTable:void 0,previewDiff:void 0,direction:"vertical",inTabs(e){return n().tabs.has(e)},replaceTab(e,s){const i=n(),t=Array.from(i.tabs.entries()),r=t.findIndex(([o])=>o===e.file);t[r]=[s.file,s],a(()=>({tabs:new Map(t)})),i.updateStoredTabsIds()},updateStoredTabsIds(){const e=n();if(d(e.tab)){b({id:void 0,tabs:[]}),a(()=>({storedTabId:void 0,storedTabs:[]}));return}const s=[];for(const t of e.tabs.values())I(t.file.isChanged)&&t.file.isLocal||s.push({id:t.file.id,content:t.file.isChanged?t.file.content:void 0});const i=e.tab.file.isChanged||e.tab.file.isRemote?e.tab.file.id:void 0;b({id:i,tabs:s}),a(()=>({storedTabId:i,storedTabs:s}))},refreshTab(e){d(e)||n().selectTab({...e})},setDialects(e){a(()=>({dialects:e}))},selectTab(e){const s=n();a(()=>({tab:e})),s.updateStoredTabsIds()},addTabs(e){const s=n();for(const i of e)s.tabs.set(i.file,i);a(()=>({tabs:new Map(s.tabs)}))},addTab(e){const s=n();if(s.tabs.has(e.file))s.tabs.set(e.file,e),a(()=>({tabs:new Map(s.tabs)}));else{const i=Array.from(s.tabs.entries()),t=i.findIndex(([r])=>{var o;return r===((o=s.tab)==null?void 0:o.file)});i.splice(t<0?i.length:t+1,0,[e.file,e]),a(()=>({tabs:new Map(i)}))}s.updateStoredTabsIds()},closeTab(e){var i;const s=n();if(e.removeChanges(),s.tabs.delete(e),s.tabs.size===0)s.selectTab(void 0);else if(s.tabs.size===1){const t=Array.from(s.tabs.values());s.selectTab(t.at(0))}else if(e.id===((i=s.tab)==null?void 0:i.file.id)){const t=Array.from(s.tabs.values()),r=t.findIndex(o=>o.file===e);s.selectTab(t.at(r-1))}a(()=>({tabs:new Map(s.tabs)})),s.updateStoredTabsIds()},createTab:T,setPreviewQuery(e){a(()=>({previewQuery:e}))},setPreviewTable(e){a(()=>({previewTable:e}))},setPreviewDiff(e){a(()=>({previewDiff:e}))},setDirection(e){a(()=>({direction:e}))}}));function T(a=p()){return{id:h(),file:a,isValid:!0}}function p(a){return new S({id:a,name:"",path:"",content:`-- Create arbitrary SQL queries
-- and execute them against different environments

`})}export{L as a,p as c,x as s,C as u};
