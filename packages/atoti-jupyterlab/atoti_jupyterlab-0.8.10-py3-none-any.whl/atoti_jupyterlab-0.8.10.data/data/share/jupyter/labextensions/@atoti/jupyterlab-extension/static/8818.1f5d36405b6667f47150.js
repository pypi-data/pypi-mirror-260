"use strict";(self.webpackChunk_atoti_jupyterlab_extension=self.webpackChunk_atoti_jupyterlab_extension||[]).push([[8818],{28818:(e,t,a)=>{a.d(t,{FiltersBarDateRangePicker:()=>p});var r=a(17967),n=a(58736),s=a(9617),i=a(27860),l=a.n(i),c=a(85578),o=a(54935),d=a(94280);const g=s.DatePicker.RangePicker,p=({filter:e,onFilterChanged:t})=>{const a=(0,o.Fg)(),{startDate:s,endDate:i}=e;return(0,r.tZ)(d.I,{levelName:e.levelName,children:(0,r.BX)("div",{css:n.css`
          display: flex;
          align-items: center;
          border: 1px solid ${a.grayScale[5]};
          border-radius: 2px;
          height: 33px;
        `,children:[e.isExclusionFilter&&(0,r.tZ)(c.IconExclude,{style:{marginLeft:3,marginRight:5}}),(0,r.tZ)(g,{css:n.css`
            margin: 0 4px 0 0;
          `,value:[l()(s),l()(i)],onChange:a=>{const[r,n]=a,s={...e,startDate:r.toDate(),endDate:n.toDate()};t(s)},placement:"bottomLeft",bordered:!1,allowClear:!1})]})})}}}]);