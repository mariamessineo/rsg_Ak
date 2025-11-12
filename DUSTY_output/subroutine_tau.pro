
SUBROUTINE used to compare SED with models and select the tau.

pro getmodel, lambda, fla_obs, temp,  modeltablenew
dir="../grid/"
readcol, "list.model",  namemod, f='(a)'
delta2=fltarr(n_elements(namemod))+1e+20
tempmod=fltarr(n_elements(namemod))
taumod=fltarr(n_elements(namemod))+9999

for j=0,n_elements(namemod)-1 do begin
  tempmod[j]=float(strmid(namemod[j],8,4))
  taumod[j]=float(strmid(namemod[j],0,4))
endfor

tempvec=[2600,2700,2800,2900,3000,3100,3200,3300,3400,3500,3600,3700,3800,3900,4000,4100,4200,4300,4400,4500]

for j=0,n_elements(namemod)-1 do begin
if(abs(temp-tempmod[j]) eq min(abs(temp-tempvec))) then begin
print, namemod[j], "  reading this file"
readcol, dir+namemod[j], ff,ftot,xatt,xDs,xDe,bb, f='(d,d,d,d,d,d)'
norm=where(ff gt 1.1 and ff lt 2.29)


ymodel= bb/ff
ymodel=ymodel/mean(ymodel[norm])*mean(fla_obs[0:1])
ymodel=ymodel

ftot2  = ftot/ff
ftot2=ftot2/mean(ftot2[norm])*mean(fla_obs[0:1])
ftot2=ftot2

ll=ff*10000.
bbf=planck(ll,temp)
aa=bbf/mean(bbf[norm])*mean(fla_obs[0])
bbf=aa

red = GETCOLOR('red', 101)
green = GETCOLOR('Green', 102)
blue = GETCOLOR('Blue', 103)
cyan = GETCOLOR('Cyan', 104)
orange = GETCOLOR('Orange', 105)
brown = GETCOLOR('Brown', 106)
black = GETCOLOR('Black', 107)

;#input of dusty
plot, alog10(ff),alog10(ftot2)-0.0, linestyle=2 , xtitle='log(lambda[um])',$
ytitle='log(F[W cm-2 um-1])', xr=[-1.5,2.2],xstyle=1,ystyle=1, yr=[-22,-12]

;#output of dusty
oplot, alog10(ff),alog10(ymodel)-0.0, color=green, linestyle=1  ;;dusty out

;#datapoints
oplot, alog10(lambda), alog10(Fla_obs),psym=4, color=red ;;datapoints


la=interpol(ftot2, ff, lambda)
oplot, alog10(lambda), alog10(la),psym =1, color=green
selpoint=where(lambda gt 7)
delta=abs(la-Fla_obs)
delta2[j]=total(abs(delta[selpoint]))

endif
endfor

myind=where(abs(delta2) eq min(abs(delta2)))
print, namemod(myind)
print, namemod[myind], "  reading this file"
modeltablenew=dir+namemod[myind[0]]

end
