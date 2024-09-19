<?php
require_once "loxberry_web.php";
require_once "Config/Lite.php";

// This will read your language files to the array $L
$L = LBSystem::readlanguage("language.ini");
$template_title = ucfirst($lbpplugindir);
$helplink = $L['HELP.LINK'];
$helptemplate = "#";

LBWeb::lbheader($template_title, $helplink, $helptemplate);

if ($_POST){
	// Get values from form
	$api_key = $_POST['api_key'];
	$serial = $_POST['serial'];
  	$ms_addr = $_POST['ms_addr'];
	$ms_port = $_POST['ms_port'];
	
	// Write new config file
	$cfg = new Config_Lite("$lbpconfigdir/plugin.cfg",LOCK_EX,INI_SCANNER_RAW);
	$cfg->setQuoteStrings(False);
	$cfg->set("FOXESS","API_KEY",$api_key);
	$cfg->set("FOXESS","SERIAL",$serial);
	$cfg->set("FOXESS","FORMAT","json");
	$cfg->set("MINISERVER","IPADDRESS",$ms_addr);
	$cfg->set("MINISERVER","PORT",$ms_port);
	$cfg->save();
}
else {
	// Get values from config file
	$cfg = new Config_Lite("$lbpconfigdir/plugin.cfg",LOCK_EX,INI_SCANNER_RAW);
	$api_key = $cfg['FOXESS']['API_KEY'];
	$serial = $cfg['FOXESS']['SERIAL'];
	$ms_addr = $cfg['MINISERVER']['IPADDRESS'];
  	$ms_port = $cfg['MINISERVER']['PORT'];
}

// This is the main area for your plugin
?>
<style>
.divTable{
    display: table;
    width: 100%;
}
.divTableRow {
    display: table-row;
}
.divTableHeading {
    background-color: #EEE;
    display: table-header-group;
}
.divTableCell, .divTableHead {
    border: 0px dotted #999999;
    display: table-cell;
    padding: 3px 10px;
    vertical-align: middle;
}
.divTableBody {
    display: table-row-group;
}
</style>
<h2><?=$L['TEXT.GREETING']?></h2>

<form method="post" data-ajax="false" name="main_form" id="main_form" action="./index.php">
        <div class="divTable">
            <div class="divTableBody">
                <div class="divTableRow">
                    <div class="divTableCell"><h3><?=$L['TEXT.API'].' '.$L['TEXT.SETTINGS']?></h3></div>
                </div>
                <div class="divTableRow">
									<div class="divTableCell" style="width:25%"><?=$L['TEXT.API_KEY']?></div>
									<div class="divTableCell"><input type="text" name="api_key" id="api_key" value="<?=$api_key?>"></div>
									<div class="divTableCell" style="width:25%"><span class="hint"><?=$L['HELP.API']?></span></div>
                </div>
                <div class="divTableRow">
									<div class="divTableCell"><?=$L['TEXT.SERIAL']?></div>
									<div class="divTableCell"><input type="text" name="serial" id="serial" value="<?=$serial?>"></div>
									<div class="divTableCell"><?=$L['HELP.SERIAL']?></div>
                </div>
                
                <div class="divTableRow">
									<div class="divTableCell"><h3><?=$L['TEXT.SRV'].' '.$L['TEXT.SETTINGS']?></h3></div>
                </div>
                <div class="divTableRow">
                <div class="divTableCell" style="width:25%"><?=$L['TEXT.IPADDRESS']?></div>
									<div class="divTableCell"><input type="text" name="ms_addr" id="ms_addr" value="<?=$ms_addr?>"></div>
									<div class="divTableCell" style="width:25%"><span class="hint"><?=$L['HELP.IPADDRESS']?></span></div>
                </div>
                <div class="divTableRow">
									<div class="divTableCell"><?=$L['TEXT.PORT']?></div>
									<div class="divTableCell"><input type="number" name="ms_port" id="ms_port" min="1025" max="65535" value="<?=$ms_port?>" data-validation-rule="special:number-min-max-value:1025:65535"></div>
									<div class="divTableCell"><?=$L['HELP.PORT']?></div>
                </div>
                
               
                
								<div class="divTableRow">
									<div class="divTableCell">&nbsp;</div>
									<div class="divTableCell"><input type="submit" id="do" value="<?=$L['TEXT.SAVE']?>" data-mini="true"></div>
									<div class="divTableCell"><a id="btnlogs" data-role="button" href="/admin/system/tools/logfile.cgi?logfile=plugins/foxess/foxess.log&header=html&format=template" target="_blank" data-inline="true" data-mini="true" data-icon="action"><?=$L['TEXT.LOGFILE']?></a></div>
                </div>
            </div>
        </div>
</form>

<script>
$('#main_form').validate();

$( document ).ready(function()
{
    validate_enable('#ms_port');
});
</script>

<?php
// Finally print the footer
LBWeb::lbfooter();
?>
