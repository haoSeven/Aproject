/**
 * Created by Administrator on 2017/6/5.
 */


function change() {
    var obj=document.getElementById('sele_suggest').value;
    document.getElementById('input_suggest').value=obj;
}

$(function () { $('#myModal').modal('hide')});

// 获取接受人
var selected_user = [];
function SelectUser(id) {
        var user_name = $("#"+ id +"").children().html();
        var user_id = parseInt(id.substring(5));
        var has_selected = false;
        if (selected_user.length !== 0){
             for (var sel_id in selected_user){
                 if (selected_user[sel_id] === user_id){
                   has_selected = true;
                }
            }
        }
        if (!has_selected){
            selected_user.push(user_id);
            var con = "";
            con += '<li id="sel_user_'+ user_id +'"><span>' + user_name + '</span></li>';
            $("#select_user").append(con);
            $("#"+ id +"").remove();
        }
    }

function getUser(id) {
        $.getJSON("/getreceiver", {"id": id}, function (data) {
            var con = "";
            $.each(data, function (i, value) {
                con += '<li id="user_'+ value.pk +'" onclick="SelectUser(this.id)"><span>' + value.fields.name + '</span></li>';
            });
            $("#get_user").html(con);
        })
    }