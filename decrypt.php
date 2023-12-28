<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Player</title>
</head>
<body>
<form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
    <label for="movie">Video Path:</label>
    <select name="movie" id="movie">
        <option value="thelastjedi">Star Wars: The last Jedi</option>
    </select>
    <button type="submit" name="playVideo">Play Video</button>
</form>

</body>
<?php
// $output = shell_exec('ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -allowed_extensions ALL -i "Streama.m3u8" -c copy -bsf:a aac_adtstoasc "output.mp4" 2>&1');

$videoPath = "out_dechq.m3u8";
$chaotic = shell_exec('python chaotic.py thelastjedi.mkv enc.key out.mkv');
header("Location: " . urlencode($videoPath));
?>
