fixtures = {
    "1" : {
        "url": "http://www.baidu.com/s?wd=python+%B1%E0%C2%EB%BC%EC%B2%E9",
        "date": "1291124510",
        "title": "\u767e\u5ea6\u641c\u7d22_python \u7f16\u7801\u68c0\u67e5      ",
        "shortening": "0Ax"
    }
}

function clickShortening ()
{
    var textarea = $(".shortening_textarea");
    var value = textarea.val ();
    $.ajax (
        {
            url : "/shortening/create/",
            type : "POST",
            data : {
                raw_url : value
            },
            success : function ( data )
            {
                // document.location += 
                var a = eval ( '(' + data + ')' );
                var loc = document.location;

                // if ( loc.indexOf ( "?id
                document.location = "/?id=" + a['shortening'];
            }
        }
    );
}

function insert ( data )
{
    var table = $( "tr", ".shortenings" );
    var tbody = $( "tbody", ".shortenings" );
    
    var a= 1;
}

/*
$(document.body).ready ( function () {
    insert ( fixtures['1'] )
} );
*/
