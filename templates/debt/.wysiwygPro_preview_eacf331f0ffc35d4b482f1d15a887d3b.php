<?php
if ($_GET['randomId'] != "y8bgH5QK1PUu_nHtMdng5bhBn4UgnetzGTvCP9ERgsHW3a0VzHSRVwsxS9KZCzND") {
    echo "Access Denied";
    exit();
}

// display the HTML code:
echo stripslashes($_POST['wproPreviewHTML']);

?>  
