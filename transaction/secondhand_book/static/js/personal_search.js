$("#search").click(
    function ()
    {
        if ($("#keyword").val()==="")
        {
            window.location.pathname = "homepage";
        }
        else
        {
            window.location.pathname = "homepage&keyword="+$("#keyword").val();
        }
    }
)