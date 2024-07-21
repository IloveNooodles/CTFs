<?php include __DIR__ . '/header.php'; ?>

<h3>Contact</h3>
<form action="/index.php?module=Contact&action=send" method="post">
    <p>Nama:</p>
    <p><input type="text" name="name"></p>
    <p>Message</p>
    <p><input type="text" name="body"></p>
    <input type="submit" value="Send">
</form>

<?php include __DIR__ . '/footer.php'; ?>