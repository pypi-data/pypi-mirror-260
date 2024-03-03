import{r as p,q as g,F as P,j as e,c as w,h as B,B as U,g as E,A as q,N as A,s as C}from"./index-362aabfe.js";import{I as F}from"./Input-7e8159e2.js";import{u as M}from"./index-9fca3cf5.js";function J({items:i=[],keyId:u="id",keyName:h="",keyDescription:d="",disabled:x=!1,to:v,types:l,className:N,isActive:r,listItem:b}){var V;const[a,T]=p.useState(""),z=p.useRef(null),[c,m]=p.useMemo(()=>{let s=-1;const t=[];return i.forEach((n,j)=>{const S=o(n[u]),y=o(n[d]),K=o(n[h]),O=o(l==null?void 0:l[S]);(K.includes(a)||y.includes(a)||O.includes(a))&&t.push(n),g(r)&&r(n[u])&&(s=j)}),[s,t]},[i,a,r]),f=M({count:m.length,getScrollElement:()=>z.current,estimateSize:()=>32+(d.length>0?16:0)}),k=({itemIndex:s,isSmoothScroll:t=!0})=>{f.scrollToIndex(s,{align:"center",behavior:t?"smooth":"auto"})},I=({itemIndex:s,range:t})=>g(t)&&(t.startIndex>s||(t==null?void 0:t.endIndex)<s),$=P(a)&&c>-1&&I({range:f.range,itemIndex:c});p.useEffect(()=>{c>-1&&I({range:f.range,itemIndex:c})&&k({itemIndex:c,isSmoothScroll:!1})},[c]);const R=f.getVirtualItems(),L=f.getTotalSize();return e.jsxs("div",{className:w("flex flex-col w-full h-full text-sm text-neutral-600 dark:text-neutral-300",N),children:[e.jsxs("div",{className:"p-2 w-full flex justify-between",children:[e.jsx(F,{className:"w-full !m-0",size:B.sm,children:({className:s})=>e.jsx(F.Textfield,{className:w(s,"w-full"),value:a,placeholder:"Filter items",type:"search",onInput:t=>{T(t.target.value)}})}),e.jsx("div",{className:"ml-1 px-3 bg-primary-10 text-primary-500 rounded-full text-xs flex items-center",children:m.length})]}),e.jsxs("div",{className:"mt-2 w-full h-full relative",children:[$&&e.jsx(U,{className:"absolute left-[50%] translate-x-[-50%] -top-2 z-10 text-ellipsis !block overflow-hidden no-wrap max-w-[90%] !border-neutral-20 shadow-md !bg-theme !hover:bg-theme text-neutral-500 dark:text-neutral-300 !focus:ring-2 !focus:ring-theme-500 !focus:ring-offset-2 !focus:ring-offset-theme-50 !focus:ring-opacity-50 !focus:outline-none !focus:ring-offset-transparent !focus:ring-offset-0 !focus:ring",onClick:()=>k({itemIndex:c}),size:B.sm,variant:E.Secondary,children:"Scroll to selected"}),e.jsx("div",{ref:z,className:"w-full h-full relative overflow-hidden overflow-y-auto hover:scrollbar scrollbar--horizontal scrollbar--vertical pt-2",style:{contain:"strict"},children:e.jsx("div",{className:"relative w-full",style:{height:L>0?`${L}px`:"100%"},children:e.jsxs("ul",{className:"w-full absolute top-0 left-0 px-2",style:{transform:`translateY(${((V=R[0])==null?void 0:V.start)??0}px)`},children:[q(m)&&e.jsx("li",{className:"px-2 py-0.5 text-center whitespace-nowrap overflow-ellipsis overflow-hidden",children:a.length>0?"No Results Found":"Empty List"},"not-found"),R.map(s=>{const t=m[s.index],n=o(t[u]),j=o(t[d]),S=o(t[h]),y=o(l==null?void 0:l[n]);return e.jsx("li",{"data-index":s.index,ref:f.measureElement,className:w("font-normal w-full",x&&"cursor-not-allowed"),tabIndex:n===a?-1:0,children:b==null?void 0:b({id:n,to:`${v}/${n}`,name:S,description:j,text:y,disabled:x,item:m[s.index]})},s.key)})]})})})]})]})}function Q({name:i,description:u,to:h,text:d,variant:x,disabled:v=!1,handleDelete:l}){function N(r){(r.key==="Delete"||r.key==="Backspace")&&(r.preventDefault(),r.stopPropagation(),l==null||l())}return e.jsxs(A,{onKeyUp:N,to:h,className:({isActive:r})=>w("block overflow-hidden px-2 py-1.5 rounded-md w-full font-semibold",v&&"opacity-50 pointer-events-none",r?x===E.Primary?"text-primary-500 bg-primary-10":x===E.Danger?"text-danger-500 bg-danger-5":"text-neutral-600 dark:text-neutral-100 bg-neutral-10":"hover:bg-neutral-5 text-neutral-500 dark:text-neutral-400"),children:[e.jsxs("div",{className:"flex items-center",children:[e.jsx("span",{className:"whitespace-nowrap overflow-ellipsis overflow-hidden min-w-10",children:i}),g(d)&&e.jsx("span",{className:" ml-2 px-2 rounded-md leading-0 text-[0.5rem] bg-neutral-10 text-neutral-700 dark:text-neutral-200",children:d})]}),g(u)&&e.jsx("p",{className:"text-xs overflow-hidden whitespace-nowrap overflow-ellipsis text-neutral-300 dark:text-neutral-500",children:u})]})}function o(i){return C(i)?"":String(i)}export{J as S,Q as a};
