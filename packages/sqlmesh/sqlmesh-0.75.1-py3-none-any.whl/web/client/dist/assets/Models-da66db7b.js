import{t as v,J as E,o as F,a as m,r as p,p as P,s as c,q as u,j as s,a4 as k,C as A,d as I,h as w,D as B,K as C,O,E as R}from"./index-362aabfe.js";import{S as b}from"./SearchList-6e46a9cf.js";import{P as z}from"./Page-03e116f0.js";import{S as D,a as T}from"./SourceList-0e3438a5.js";import{g as q}from"./context-8772d184.js";import{u as f}from"./project-a0cf4288.js";import"./Input-7e8159e2.js";import"./transition-9d91db7c.js";import"./SplitPane-7090afa7.js";import"./index-9fca3cf5.js";import"./_commonjs-dynamic-modules-302442b1.js";import"./editor-33420b17.js";import"./file-c1b8e58b.js";function se({route:x=R.Home}){const{pathname:g}=v(),{modelName:a}=E(),y=F(),n=m(e=>e.models),i=m(e=>e.lastSelectedModel),N=m(e=>e.setLastSelectedModel),d=f(e=>e.files),j=f(e=>e.setSelectedFile),r=p.useMemo(()=>Array.from(new Set(n.values())),[n]),{isFetching:S}=P(),t=`${x}/models`,o=c(a)||a===(i==null?void 0:i.name)?i:n.get(encodeURI(a));p.useEffect(()=>{if(c(o))return;const e=d.get(o.path);u(e)&&j(e),N(o),y(`${t}/${o.name}`,{replace:!0})},[d,o,t]);const h=c(o)&&u(a);return S?s.jsx(k,{children:"Loading Models..."}):s.jsx(z,{sidebar:s.jsx(D,{keyId:"displayName",keyName:"displayName",to:t,items:r,isActive:e=>`${t}/${e}`===g,types:r.reduce((e,l)=>Object.assign(e,{[l.name]:q(l.type)}),{}),listItem:({to:e,name:l,description:M,text:L,disabled:$=!1})=>s.jsx(T,{to:e,name:l,text:L,description:M,disabled:$})}),content:s.jsx(A.Page,{children:s.jsxs("div",{className:"flex flex-col w-full h-full overflow-hidden",children:[I(r)&&s.jsx(b,{list:r,size:w.lg,searchBy:"index",displayBy:"displayName",to:e=>`${t}/${e.name}`,direction:"top",className:"my-2",isFullWidth:!0}),s.jsx(B,{}),h?s.jsx(C,{link:t,message:"Go Back",description:`Model "${a}" not found.`}):s.jsx(O,{})]})})})}export{se as default};
