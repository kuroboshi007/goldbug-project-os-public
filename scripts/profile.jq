def known($o; $allowed):
  ($o | type) == "object" and ((($o | keys) - $allowed) | length) == 0;
def optional_known($o; $key; $allowed):
  if $o | has($key) then known($o[$key]; $allowed) else true end;
def optional_type($o; $key; $t):
  if $o | has($key) then ($o[$key] | type) == $t else true end;
def text($v): ($v | type) == "string" and ($v | length) > 0;
def types($o; $strings; $bools):
  all($strings[]; optional_type($o; .; "string")) and
  all($bools[]; optional_type($o; .; "boolean"));
. as $p |
if ($p | type) != "object" then "invalid profile"
elif $p.schema_version != 1 then "unsupported schema_version"
elif ((known($p; ["schema_version","maintainer","commit_email","language","timezone","notes","upstream","registry","shared_services"]) and
      optional_known($p; "maintainer"; ["name","mark","handle"]) and
      optional_known($p; "commit_email"; ["enforce","address"]) and
      optional_known($p; "language"; ["operational","summaries"]) and
      optional_known($p; "notes"; ["mode","notion","markdown"]) and
      optional_known(($p.notes // {}); "notion"; ["home_page","status_page","portfolio_database","articles_database","schema_fields"]) and
      optional_known(($p.notes.notion // {}); "portfolio_database"; ["id","name"]) and
      optional_known(($p.notes.notion // {}); "articles_database"; ["id","name"]) and
      optional_known(($p.notes.notion // {}); "schema_fields"; ["status","type","perspective","start_date","repo","source","updated","project"]) and
      optional_known(($p.notes // {}); "markdown"; ["destination_folder"]) and
      optional_known($p; "upstream"; ["url","sibling_checkout"]) and
      optional_known($p; "registry"; ["path","portfolio_exists"]) and
      optional_known($p; "shared_services"; ["announcement_channel"]) and
      optional_known(($p.shared_services // {}); "announcement_channel"; ["enabled","how_to_url"])) | not)
then "unknown key or invalid object"
elif ((types(($p.maintainer // {}); ["name","mark","handle"]; []) and
      types(($p.commit_email // {}); ["address"]; ["enforce"]) and
      types(($p.language // {}); ["operational","summaries"]; []) and
      optional_type($p; "timezone"; "string") and
      types(($p.notes // {}); ["mode"]; []) and
      types(($p.notes.notion // {}); ["home_page","status_page"]; []) and
      types(($p.notes.notion.portfolio_database // {}); ["id","name"]; []) and
      types(($p.notes.notion.articles_database // {}); ["id","name"]; []) and
      types(($p.notes.notion.schema_fields // {}); ["status","type","perspective","start_date","repo","source","updated","project"]; []) and
      types(($p.notes.markdown // {}); ["destination_folder"]; []) and
      types(($p.upstream // {}); ["url","sibling_checkout"]; []) and
      types(($p.registry // {}); ["path"]; ["portfolio_exists"]) and
      types(($p.shared_services.announcement_channel // {}); ["how_to_url"]; ["enabled"])) | not)
then "invalid field type"
elif (($p.maintainer | has("mark")) and
      (($p.maintainer.mark | test("^[A-Za-z]$")) | not)) then "invalid maintainer mark"
elif (($p.maintainer.mark // "M" | ascii_upcase) as $mark | $mark == "C" or $mark == "X") then "reserved maintainer mark"
elif (["none","notion","markdown"] | index($p.notes.mode // "none") | not) then "unsupported notes mode"
elif ($p.commit_email.enforce // false) and (text($p.commit_email.address) | not) then "missing commit_email.address"
elif ($p.notes.mode // "none") == "markdown" and (text($p.notes.markdown.destination_folder) | not) then "missing markdown destination"
elif ($p.notes.mode // "none") == "notion" and
     (all([$p.notes.notion.home_page, $p.notes.notion.status_page,
           $p.notes.notion.articles_database.id, $p.notes.notion.articles_database.name,
           $p.notes.notion.schema_fields.status, $p.notes.notion.schema_fields.type,
           $p.notes.notion.schema_fields.repo, $p.notes.notion.schema_fields.source,
           $p.notes.notion.schema_fields.updated, $p.notes.notion.schema_fields.project][]; text(.)) | not)
then "missing notion destination or schema field"
elif ($p.notes.mode // "none") == "notion" and ($p.registry.portfolio_exists // false) and
     (all([$p.notes.notion.portfolio_database.id, $p.notes.notion.portfolio_database.name,
           $p.notes.notion.schema_fields.perspective, $p.notes.notion.schema_fields.start_date][]; text(.)) | not)
then "missing notion portfolio destination or schema field"
elif ($p.shared_services.announcement_channel.enabled // false) and
     (text($p.shared_services.announcement_channel.how_to_url) | not) then "missing announcement how-to"
else "valid" end
