<?php

function curlGetPage ($web)
{
   $curl = curl_init ();

   curl_setopt ($curl, CURLOPT_FOLLOWLOCATION, 1);
   curl_setopt ($curl, CURLOPT_RETURNTRANSFER, 1);
   curl_setopt ($curl, CURLOPT_URL, $web);
   curl_setopt ($curl, CURLOPT_USERAGENT, 'curl/7.21.4 (universal-apple-darwin11.0) libcurl/7.21.4 OpenSSL/0.9.8r zlib/1.2.5');

   $page = curl_exec ($curl);
   curl_close ($curl);

   echo sprintf("I sent a request to a website (%s).\n", $web);

   return $page;
}

function textSearch ($haystack, $needles)
{
   $search = array();

   foreach ($needles as $needle)
   {
      $strpos = strpos ($haystack, $needle);
      $search [$needle] = (is_bool($strpos) == false);
   }

   return $search;
}

function extractMessage ($string)
{
   $preg_match = array();
   preg_match('%<!-- message -->(.*)<!-- / message -->%s', $string, $preg_match);

   if (isset ($preg_match [1]) == false)
      { return ''; }

   $string_1 = strtolower($preg_match [1]);
   $string_2 = str_replace(array ('<', '>', '/', '\\', '"', "'", '-', '!', "\r", "\n", ':', '#', '=', '_', '?', '&', '%', '.', ',', ';', '(', ')'), ' ', $string_1);
   $string_3 = preg_replace( '/\s+/', ' ', $string_2);

   return $string_3;
}

function textSearchWords ($threads, $words)
{
   $table = array();

   foreach ($threads as $thread)
   {
      $string = curlGetPage ($thread);
      $text   = extractMessage ($string);

      $table [$thread] = textSearch ($text, $words);
   }

   return $table;
}

{
   $json_1 = json_decode (file_get_contents ('words.json'));

   if (is_null($json_1))
      { die("Invalid JSON: words.json\n"); }

   $words = $json_1->content;
}

{
   $json_2 = json_decode (file_get_contents ('boards.json'));

   if (is_null($json_2))
      { die("Invalid JSON: words.json\n"); }

   $boards = $json_2->content;
}

function getThreadsFromBoards ($boards)
{
   $numbers = array();
   $threads = array();

   foreach ($boards as $board)
   {
      $page = curlGetPage ($board);

      $preg_match = array ();
      preg_match_all ('%showthread\.php(.*?)t=(\d+)(.*?)"%s', $page, $preg_match);

      $numbers = array_merge ($numbers, $preg_match [2]);
   }

   $numbers = array_unique ($numbers);

   foreach ($numbers as $number)
      { $threads[] = sprintf('http://www.addforums.com/forums/showthread.php?t=%s', $number); }

   return $threads;
}

function getThreadsFromPages ($webs)
{
   $boards  = getBoardsFromPages ($webs);
   $threads = getThreadsFromBoards ($boards);

   $threads = array_unique ($threads);
   return $threads;
}

function getBoardsFromPages ($webs)
{
   $boards = array();
   $numbers = array();

   foreach ($webs as $web)
   {
      $page = curlGetPage ($web);

      $preg_match = array ();
      preg_match_all ('%forumdisplay\.php(.*?)f=(\d+)(.*?)"%s', $page, $preg_match);

      $numbers = array_merge ($numbers, $preg_match [2]);
   }

   $numbers = array_unique ($numbers);

   foreach ($numbers as $number)
      { $boards[] = sprintf('http://www.addforums.com/forums/forumdisplay.php?f=%s', $number); }

   return $boards;
}

$threads = getThreadsFromPages (['http://www.addforums.com/forums/index.php']);
$table   = textSearchWords ($threads, $words);

var_dump ($table);

// var_dump (textSearchWords ($threads, $words));
