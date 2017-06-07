/**
 * Created by Administrator on 2017/6/5.
 */

function change() {
    var obj=document.getElementById('sele_suggest').value;
    document.getElementById('input_suggest').value=obj;
}
$(function () { $('#myModal').modal('hide')});
function test(){
    document.getElementById('a').style.display='none';
    document.getElementById('b').style.display='none';
    document.getElementById('c').style.display='none';
    var value=document.getElementById('select').value;
    document.getElementById(value).style.display='block';
}