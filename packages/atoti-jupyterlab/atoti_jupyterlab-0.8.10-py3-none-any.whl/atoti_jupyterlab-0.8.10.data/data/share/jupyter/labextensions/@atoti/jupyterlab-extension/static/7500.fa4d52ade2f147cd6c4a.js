"use strict";(self.webpackChunk_atoti_jupyterlab_extension=self.webpackChunk_atoti_jupyterlab_extension||[]).push([[7500],{54935:(r,e,o)=>{if(o.d(e,{Fg:()=>g,f6:()=>u}),1460==o.j)var n=o(17967);var t=o(58736),a=o(9617),i=o(66029),l=o(85578);if(1460==o.j)var c=o(97097);if(1460==o.j)var s=o(66978);const d=(0,i.createContext)(null),u=r=>{const e=(0,i.useMemo)((()=>(0,s.l)(r.value)),[r.value]),o=(0,c.m)(e),u=(0,i.useMemo)((()=>({accentColor:e.primaryColor,successColor:e.successColor,warningColor:e.warningColor,errorColor:e.errorColor,whiteColor:e.backgroundColor,lightGrayColor:e.grayScale[5],darkGrayColor:e.grayScale[7]})),[e]);return(0,n.tZ)(d.Provider,{value:e,children:(0,n.tZ)(a.ConfigProvider,{theme:o,children:(0,n.tZ)(l._IconThemeContext.Provider,{value:u,children:(0,n.tZ)(a.App,{className:r.className,css:t.css`
              box-sizing: border-box;
              font-size: ${o.token?.fontSizeSM}px;
              line-height: ${o.token?.lineHeight};
              font-family: ${o.token?.fontFamily};
              color: ${o.token?.colorText};
              background-color: ${o.token?.colorBgBase};

              *,
              *:before,
              *:after {
                box-sizing: inherit;
              }

              .aui-invisible-scrollbars {
                scrollbar-width: none;
              }
              .aui-invisible-scrollbars::-webkit-scrollbar {
                display: none;
              }

              .ant-picker-dropdown {
                padding: 0;
              }
              .ant-picker-range-arrow {
                ::before,
                ::after {
                  display: none;
                }
              }

              .ant-modal-footer {
                padding-inline: ${o.components?.Modal?.paddingLG}px!important;
              }

              .ant-popconfirm-buttons {
                padding-top: ${o.components?.Popconfirm?.paddingXXS}px!important;
              }

              .ant-popover {
                .ant-popover-title {
                  border-bottom: 0px;
                }

                .ant-popover-inner-content {
                  padding: 8px 12px 8px 12px;
                }
              }

              button,
              input {
                font-family: inherit;
                line-height: inherit;
                font-size: inherit;
              }

              input[type="checkbox"] {
                margin: 0;
              }

              fieldset {
                border: none;
              }

              g.pointtext {
                display: none;
              }

              /*
           * TODO Remove when upgrading Ant Design.
           * This is an Ant Design bug fixed in https://github.com/ant-design/ant-design/commit/467741f5.
           */
              .ant-dropdown-menu-sub {
                margin: 0;
              }
            `,children:r.children})})})})};function g(){const r=(0,i.useContext)(d);if(!r)throw new Error("Missing theme. Remember to add <ThemeProvider /> at the top of your application.");return r}d.Consumer},46429:(r,e,o)=>{if(o.d(e,{$:()=>l}),1460==o.j)var n=o(71438);if(1460==o.j)var t=o(91781);if(1460==o.j)var a=o(986);const i=1460==o.j?["transparent",void 0,null]:null,l=function(r,e,o){if(i.includes(r)&&e)return(0,t.v)((0,n.h)(e),o);if(i.includes(e)&&r)return(0,t.v)((0,n.h)(r),o);if(r&&e){const t=(0,n.h)(r),i=(0,n.h)(e);return(0,a.B)(function(r,...e){return e[0].map(((o,n)=>r(...e.map((r=>r[n])))))}(((r,e)=>Math.ceil((1-o)*r+o*e)),t,i))}throw new Error("Invalid arguments to addColorLayer")}},72550:(r,e,o)=>{o.d(e,{a:()=>i});var n=o(71438),t=o(91781);const a=/\d+(\.\d*)?|\.\d+/g,i=function({color:r,opacity:e,shadeFactor:o=0,isShading:i,isInverting:l}){const c=(0,n.h)(r),s=r.startsWith("rgba")?(r=>{const e=r.match(a);if(!e)throw new SyntaxError("Invalid rgba parameter");return Number.parseFloat(e.slice(3).join(""))})(r):1;return(0,t.v)(c.map((r=>{const e=l?(r=>255-r)(r):r;return n=i?e*(1-o):e+(255-e)*o,Math.max(0,Math.min(255,n));var n})),(d=s*e,Math.max(0,Math.min(1,d))));var d}},2360:(r,e,o)=>{if(o.d(e,{f:()=>t}),1460==o.j)var n=o(46429);const t=(r,e)=>{const o=o=>(0,n.$)(r,e,o);return[o(0),o(.02),o(.04),o(.06),o(.09),o(.15),o(.25),o(.45),o(.55),o(.65),o(.75),o(.85),o(.95),o(1)]}},97097:(r,e,o)=>{o.d(e,{m:()=>t});var n=o(9617);function t(r){return{token:{lineHeight:1.66667,fontSizeSM:12,fontFamily:"-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, Noto Sans, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol, Noto Color Emoji",borderRadius:2,controlOutlineWidth:0,colorPrimary:r.primaryColor,colorSuccess:r.successColor,colorWarning:r.warningColor,colorText:r.textColor,colorTextPlaceholder:r.placeholderColor,colorTextDisabled:r.disabledTextColor,colorBgBase:r.backgroundColor,colorPrimaryBg:r.selectedMenuItemBackground,colorBgContainerDisabled:r.disabledBackground,colorBorder:r.cellBorderColor,colorBorderSecondary:r.cellBorderColor},components:{Menu:{radiusItem:0,radiusSubMenuItem:0,lineWidth:.5,margin:12,controlHeightLG:32,colorActiveBarBorderSize:0,colorActiveBarWidth:3,colorItemTextSelected:r.primaryColor,colorSubItemBg:r.menuInlineSubmenuBg},Tooltip:{paddingXS:8,paddingSM:12},Checkbox:{paddingXS:8},Modal:{wireframe:!0,paddingXS:8,marginXS:8,padding:11,paddingLG:16},Popover:{wireframe:!0,padding:12,paddingSM:12},Popconfirm:{marginXS:8,paddingXXS:4},Card:{padding:8.5,paddingLG:12,fontWeightStrong:500},Dropdown:{marginXS:8,controlPaddingHorizontal:8},Tabs:{colorText:r.grayScale[8],colorFillAlter:r.grayScale[3]}},algorithm:[n.theme.compactAlgorithm,...r.isDark?[n.theme.darkAlgorithm]:[],(r,e=n.theme.defaultAlgorithm(r))=>({...e,colorInfo:r.colorPrimary,colorBgContainer:r.colorBgBase,colorBgElevated:r.colorBgBase,colorBgLayout:r.colorBgBase})]}}},66978:(r,e,o)=>{o.d(e,{l:()=>c});var n=o(26274);if(1460==o.j)var t=o(2360);if(1460==o.j)var a=o(1347);if(1460==o.j)var i=o(30191);if(1460==o.j)var l=o(31623);function c(r){const e=!Boolean(r.isDark),o=r.white??e?"#FFFFFF":"#000000",c=r.black??e?"#000000":"#FFFFFF",s=r.backgroundColor??o,d=(0,t.f)(s,c),u=(0,l.w)([(0,i.k)(r.primaryColor)[0],"100","50"]),g=r.successColor??"#52C41A",m=r.errorColor??"#F5222D",p=(0,n.R_)(r.primaryColor,{theme:e?"default":"dark",backgroundColor:s});return{activeMenuItemBackgroundColor:d[4],activeTabBackgroundColor:d[0],alternateCellBackgroundColor:(0,a.U)(d[2],.65),alternateBackgroundColor:d[1],backgroundColor:s,black:c,cellBackgroundDuringNegativeTransition:(0,a.U)(m,.7),cellBackgroundDuringPositiveTransition:(0,a.U)(g,.7),cellBorderColor:d[5],headerActiveColor:r.primaryColor,disabledBackground:e?"#F5F5F5":s,disabledTextColor:e?(0,a.U)(c,.35):(0,a.U)(c,.25),dropHintBorderColor:(0,a.U)(u,.2),dropHintColor:(0,a.U)(u,.15),errorColor:m,grayScale:d,hoverColor:p[5],inactiveTabBackgroundColor:d[2],menuInlineSubmenuBg:"transparent",placeholderColor:d[6],primaryScale:p,selectedMenuItemBackground:p[0],selectionOverlayColor:(0,a.U)(u,.1),selectionMarkDarkColor:"#646464",selectionMarkLightColor:"#FFFFFF",selectionColor:p[0],shadowColor:"#000C11",successColor:g,textColor:e?d[11]:(0,a.U)(c,.65),warningColor:"#FAAD14",white:o,...r}}},71438:(r,e,o)=>{function n(r,e,o){const n=(o+1)%1;return n<1/6?r+6*(e-r)*n:n<.5?e:n<2/3?r+(e-r)*(2/3-n)*6:r}o.d(e,{h:()=>i});const t=/\d+/g,a=/\d+(\.\d*)?|\.\d+/g,i=function(r){const e=r.toLowerCase();if(e.startsWith("#"))return function(r){if(6!==r.length&&3!==r.length)throw new Error(`Hex color (${r}) is not a valid 3 or 6 character string`);const e=6===r.length?r:r.charAt(0).repeat(2)+r.charAt(1).repeat(2)+r.charAt(2).repeat(2);return[Number.parseInt(e.slice(0,2),16),Number.parseInt(e.slice(2,4),16),Number.parseInt(e.slice(4,6),16)]}(r.slice(1));if(e.startsWith("rgb"))return(r=>{const e=r.match(t);if(!e)throw new SyntaxError("Invalid rgb parameter");const o=e.slice(0,3).map((r=>Number(r)));return[o[0],o[1],o[2]]})(r);if(e.startsWith("hsl"))return(r=>{const e=r.match(a);if(!e)throw new SyntaxError("Invalid hsl parameter");const o=e.slice(0,3).map((r=>Number(r)));return function(r,e,o){let t,a,i;const l=r/360,c=e/100,s=o/100;if(0===c)i=s,a=s,t=s;else{const r=s<.5?s*(1+c):s+c-s*c,e=2*s-r;t=n(e,r,l+1/3),a=n(e,r,l),i=n(e,r,l-1/3)}return t=Math.round(255*t),a=Math.round(255*a),i=Math.round(255*i),[t,a,i]}(o[0],o[1],o[2])})(r);throw new Error("Unsupported color syntax. Supported syntaxes are rgb, hsl and hex.")}},1347:(r,e,o)=>{o.d(e,{U:()=>t});var n=o(72550);function t(r,e=1){return(0,n.a)({color:r,opacity:e})}},43824:(r,e,o)=>{function n(r,e,o){const n=r/255,t=e/255,a=o/255,i=Math.max(n,t,a),l=Math.min(n,t,a);let c=0,s=0,d=(i+l)/2;if(i!==l){const r=i-l;switch(s=d>.5?r/(2-i-l):r/(i+l),i){case n:c=(t-a)/r+(t<a?6:0);break;case t:c=(a-n)/r+2;break;case a:c=(n-t)/r+4}c/=6}return c=Math.round(360*c),s=Math.round(100*s),d=Math.round(100*d),[c,s,d]}o.d(e,{l:()=>n})},30191:(r,e,o)=>{if(o.d(e,{k:()=>a}),1460==o.j)var n=o(71438);if(1460==o.j)var t=o(43824);function a(r){return(0,t.l)(...(0,n.h)(r))}},31623:(r,e,o)=>{function n(r){return`hsl(${r[0]}, ${r[1]}%, ${r[2]}%)`}o.d(e,{w:()=>n})},91781:(r,e,o)=>{o.d(e,{v:()=>n});const n=function(r,e){return`rgba(${r.join(", ")}, ${e})`}},986:(r,e,o)=>{o.d(e,{B:()=>n});const n=function(r){return`rgb(${r.join(", ")})`}},59401:(r,e,o)=>{o.d(e,{N:()=>t});const n=new Set;function t(r,e){n.has(r)||(n.add(r),console.warn(`%c ${r} `,"font-style: italic; border: 1px solid orange; border-radius: 5px","is deprecated and will not be supported in the next breaking release of Atoti UI.",e))}},24958:(r,e,o)=>{o.d(e,{C:()=>f,E:()=>F,T:()=>b,_:()=>v,a:()=>k,b:()=>S,c:()=>B,h:()=>p,i:()=>m,u:()=>x,w:()=>C});var n=o(66029),t=o(21759),a=o(77587),i=o(72609),l=o(10063),c=o.n(l),s=function(r,e){return c()(r,e)},d=o(68116),u=o(93232),g=o(78070),m=!0,p={}.hasOwnProperty,h=n.createContext("undefined"!=typeof HTMLElement?(0,t.Z)({key:"css"}):null),f=h.Provider,v=function(){return(0,n.useContext)(h)},C=function(r){return(0,n.forwardRef)((function(e,o){var t=(0,n.useContext)(h);return r(e,t,o)}))};m||(C=function(r){return function(e){var o=(0,n.useContext)(h);return null===o?(o=(0,t.Z)({key:"css"}),n.createElement(h.Provider,{value:o},r(e,o))):r(e,o)}});var b=n.createContext({}),x=function(){return n.useContext(b)},y=(0,i.Z)((function(r){return(0,i.Z)((function(e){return function(r,e){return"function"==typeof e?e(r):(0,a.Z)({},r,e)}(r,e)}))})),k=function(r){var e=n.useContext(b);return r.theme!==e&&(e=y(e)(r.theme)),n.createElement(b.Provider,{value:e},r.children)};function S(r){var e=r.displayName||r.name||"Component",o=function(e,o){var t=n.useContext(b);return n.createElement(r,(0,a.Z)({theme:t,ref:o},e))},t=n.forwardRef(o);return t.displayName="WithTheme("+e+")",s(t,r)}var w="__EMOTION_TYPE_PLEASE_DO_NOT_USE__",B=function(r,e){var o={};for(var n in e)p.call(e,n)&&(o[n]=e[n]);return o[w]=r,o},M=function(r){var e=r.cache,o=r.serialized,n=r.isStringTag;return(0,d.hC)(e,o,n),(0,g.L)((function(){return(0,d.My)(e,o,n)})),null},F=C((function(r,e,o){var t=r.css;"string"==typeof t&&void 0!==e.registered[t]&&(t=e.registered[t]);var a=r[w],i=[t],l="";"string"==typeof r.className?l=(0,d.fp)(e.registered,i,r.className):null!=r.className&&(l=r.className+" ");var c=(0,u.O)(i,void 0,n.useContext(b));l+=e.key+"-"+c.name;var s={};for(var g in r)p.call(r,g)&&"css"!==g&&g!==w&&(s[g]=r[g]);return s.ref=o,s.className=l,n.createElement(n.Fragment,null,n.createElement(M,{cache:e,serialized:c,isStringTag:"string"==typeof a}),n.createElement(a,s))}))},17967:(r,e,o)=>{o.d(e,{BX:()=>l,HY:()=>a,tZ:()=>i});var n=o(97458),t=o(24958),a=(o(66029),o(21759),o(10063),o(93232),o(78070),n.Fragment);function i(r,e,o){return t.h.call(e,"css")?n.jsx(t.E,(0,t.c)(r,e),o):n.jsx(r,e,o)}function l(r,e,o){return t.h.call(e,"css")?n.jsxs(t.E,(0,t.c)(r,e),o):n.jsxs(r,e,o)}}}]);