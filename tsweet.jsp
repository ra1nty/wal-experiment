import { open, fill, click, find} from './library';
crns = [1,2,3]
url1 = "https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1"
open url1
fill "#netid" "yutang2"
fill "#easpass" "19970202"
click ".bttn"
semester = "111111"
for(crn in crns){
    url = "https://ui2web1.apps.uillinois.edu/BANPROD1/bwckschd.p_disp_detail_sched?term_in="+semester+"&crn_in="+crn
    open url
    remain = find "//td[@class='dddefault'][3]"
    if(remain){
        open "https://ui2web1.apps.uillinois.edu/BANPROD1/twbkwbis.P_GenMenu?name=bmenu.P_RegAgreementAdd"
        sel = "//option[@value='"+semester+"']"
        click sel
        click "I Agree"
        fill "#crn_id1" crn
        click "//input[@value='Submit Changes']"
    }
}