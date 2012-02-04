/**
 * Created by PyCharm.
 * User: ben
 * Date: 1/19/12
 * Time: 11:40 AM
 * To change this template use File | Settings | File Templates.
 */
var activeCell;
var oldContents;
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
$(document).ready(function () {
    $("td").click(function (e) {
        if (e.target.tagName != "TD") return;
        var col = $(this).parent().children().index($(this));
        var row = $(this).parent().parent().children().index($(this).parent());
        if (row>0 && col>0) {
            if (row != col) {
                if ($(e.target).html() == "0") {
                    alert("No debt to settle");
                    return;
                } else if (e.target != activeCell) {
                    $.post("/ajax/getmemos/",{
                       id1:(col),
                       id2:(row)
                    },function(response) {
                        $("#memos").slideUp(300,function() {
                            $("#memos").html("");
                            for (var i=0;i<response.length;i++) {
                                var dir = "owes";
                                if (response[i].dir == -1) {
                                    dir = "paid";
                                }
                                var newMemo = document.createElement("div");
                                newMemo.className = "payment";
                                var dateDiv = document.createElement("span");
                                dateDiv.innerHTML = "Date: "+response[i].date;
                                var bodyDiv = document.createElement("div");
                                bodyDiv.innerHTML = response[i].payer + " "+dir+" "+response[i].payee + " $"+response[i].amount+"<br />";
                                bodyDiv.innerHTML += "Memo: "+response[i].memo;
                                var form = "<a href='/debts/remove/"+response[i].id+"' class='btn primary'>Remove Item</a>";
                                $(newMemo).append(dateDiv);
                                $(newMemo).append(bodyDiv);
                                $(newMemo).append(form);
                                $("#memos").append(newMemo);
                            }
                            $("#memos").slideDown(300);
                        });
                    },"json");
                    if (activeCell) {
                        //$(activeCell).html(oldContents);
                        $(activeCell).find("div").toggle();
                        var curHeight = $(activeCell).height();
                        var curWidth = $(activeCell).width();
                        $(activeCell).css('width','auto');
                        $(activeCell).css('height','auto');
                        var autoHeight = $(activeCell).height();
                        var autoWidth = $(activeCell).width();
                        $(activeCell).find("div").toggle();
                        $(activeCell).find("div").slideUp(250,function() {
                            $(activeCell).find("div").remove();
                            $(activeCell).height(curHeight).width(curWidth).animate({
                                width:autoWidth,
                                height:autoHeight
                            },250,function() {
                                activeCell = e.target;
                                var el = "<a href='/debts/settle/"+row+"/"+col+"/' class='btn primary'>Settle Debt</a>"
                                var formdiv = document.createElement("div");

                                $(formdiv).append(el);
                                //$(formdiv).append(em);
                                $(e.target).append(formdiv);
                                var w = $(e.target).width();
                                var h = $(e.target).height();
                                $(e.target).find("div").toggle();
                                //$(br).toggle();
                                //$(el).slideToggle();
                                $(e.target).animate({
                                    width: w,
                                    height: h
                                },250, function() {
                                    $(e.target).find("div").slideToggle(250);
                                    //$(activeCell).attr('style','');
                                });
                            });
                        });
                    } else {
                        activeCell = e.target;
                        var el = "<a href='/debts/settle/"+row+"/"+col+"/' class='btn primary'>Settle Debt</a>"
                        var formdiv = document.createElement("div");
                        $(formdiv).append(el);
                        //$(formdiv).append(em);
                        $(e.target).append(formdiv);
                        var w = $(e.target).width();
                        var h = $(e.target).height();
                        $(e.target).find("div").toggle();
                        //$(br).toggle();
                        //$(el).slideToggle();
                        $(e.target).animate({
                            width: w,
                            height: h
                        },250, function() {
                            $(e.target).find("div").slideToggle(250);
                            //$(activeCell).attr('style','');
                        });
                    }
                }
            } else {
                alert("Null cell");
            }
        }
    });
});