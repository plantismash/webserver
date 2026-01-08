function toggle_clusters() {
    var id = 2;
    var value_to_set = $('#cluster_1').prop('checked');
    if (!value_to_set) {
        value_to_set = false;
    }
    while($('#cluster_' + id).length) {
        $('#cluster_' + id).prop('checked', value_to_set);
        id++;
    }
}

function toggle_region() {
    if ($('#region').prop('checked')) {
        $('#region-input').show("fast");
    } else {
        $('#region-input').hide("fast");
    }
}

function toggle_legacy() {
    if ($('#legacy').prop('checked')) {
        $('#cluster_1').prop("checked", true);
        var id = 2;
        while($('#cluster_' + id).length) {
            $('#cluster_' + id).attr("disabled", true);
            id++;
        }
        $('#subclusterblast').prop("checked", false);
        $('#subclusterblast').attr("disabled", true);
        $('#inclusive').prop("checked", false);
        $('#inclusive').attr("disabled", true);
    } else {
        var id = 2;
        while($('#cluster_' + id).length) {
            $('#cluster_' + id).attr("disabled", false);
            id++;
        }
        $('#subclusterblast').prop("checked", true);
        $('#subclusterblast').attr("disabled", false);
        $('#inclusive').attr("disabled", false);
    }
}

function toggle_cassis_tip() {
    if ($('#eukaryotic').prop("checked")) {
        $('#cassis-link').show();
    } else {
        $('#cassis-link').hide();
    }
}

function clear_upload() {
    $('#seq').val('');
    show_genefinding_if_needed();
}

function clear_ncbi() {
    $('#ncbi').val('');
}

function clear_sequence() {
    $('#sequence').val('');
}

function clear_prot_ncbi() {
    $('#prot-ncbi').val('');
}

function show_genefinding_if_needed() {
    var file = $('#seq').val();
    var euc  = $('#eukaryotic').prop('checked');

    fasta = is_fasta(file);
    if ( fasta && !euc) {
        show_genefinding();
    } else {
        hide_genefinding();
    }
    show_glimmer_if_needed(fasta, euc);
}


function show_glimmer_if_needed(fasta, euc) {
    var genefinder = $('input[name=genefinder]:checked').val();

    // No need to show glimmer settings for eukaryotic fasta files
    if( fasta && genefinder == 'glimmer' && !euc ) {
        show_glimmer();
    } else {
        hide_glimmer();
    }
}


function seq_callback() {
    clear_ncbi();
    show_gff_upload_if_unannotated();
}

function show_gff_upload_if_unannotated() {
  var display = "none";
  if (get_ext($('#seq').val().toLowerCase()).length > 0) {
    display = "";
  }
  $('#gff-row').css("display", display);
}

function show_genefinding() {
    $('.dna_related').each(function(){
        $(this).show("fast");
    });
}
function show_glimmer() {
    $('.glimmer').each(function(){
        $(this).show("fast");
    });
}

function hide_genefinding() {
    $('.dna_related').each(function(){
        $(this).hide("fast");
    });
}

function hide_glimmer() {
    $('.glimmer').each(function(){
        $(this).hide("fast");
    });
}

function get_ext(file) {
    return file.split('.').pop();
}

function is_annotated(file) {
    var ext = get_ext(file.toLowerCase());
    var valid_exts = ['gb', 'gbk', 'gbff' , 'genbank', 'emb', 'embl'];
    var res = false;
    for (var i in valid_exts) {
        if (ext == valid_exts[i]) {
            res = true;
            break;
        }
    }
    return res;
}

function is_fasta(file) {
    var ext = get_ext(file.toLowerCase());
    var valid_exts = ['fasta', 'fas', 'fa', 'fna'];
    var res = false;
    for (var i in valid_exts) {
        if (ext == valid_exts[i]) {
            res = true;
            break;
        }
    }
    return res;
}

function is_gff3(file) {
    var ext = get_ext(file.toLowerCase());
    var valid_exts = ['gff', 'gff3', 'gtf'];
    var res = false;
    for (var i in valid_exts) {
        if (ext == valid_exts[i]) {
            res = true;
            break;
        }
    }
    return res;
}

function is_valid_coexpress(file) {
    var ext = get_ext(file.toLowerCase())
    var valid_exts = ['soft', 'csv']
    var res = false;
    for (var i in valid_exts) {
        if (ext == valid_exts[i]) {
            res = true;
            break;
        }
    }
    return res;
}

function getFileSize() {
    var input, file;

    if (typeof window.FileReader !== 'function') {
        return 0;
    }

    input = $('#file');
    if (!input) {
        return 0;
    }
    else if (!input.files) {
        return 0;
    }
    else {
        file = input.files[0];
        return file.size;
    }
}

function verify_nucl_form() {
    var file = $('#seq').val();
    var ncbi = $('#ncbi').val();
    var gff = $('#gff').val();
    var coexpress = $('#coexpress_file').val();

    if( (file === '' || file === null) && (ncbi === '' || ncbi === null)){
        alert('No input file provided. Please enter NCBI number or upload your own file');
        return false;
    }

    if( !(is_annotated(file) || is_fasta(file)) && ncbi === '' ) {
        alert('Please provide EMBL/GenBank or nucleotide FASTA file');
        return false;
    } else if ( is_fasta(file) && !is_gff3(gff) ) {
        alert('Please provide annotation file (GFF3 format)');
        return false;
    } else if ( !is_valid_coexpress(coexpress) ) {
        alert('Please provide coexpress file (SOFT or csv format)');
        return false;
    }

    return true;
}

function verify_prot_form() {
    var sequence = $('#sequence').val();
    var ncbi = $('#prot-ncbi').val();

    if( (sequence === '') && (ncbi === '')){
        alert('No input provided. Please enter NCBI number or paste your own sequence');
        return false;
    }

    if (ncbi.indexOf(';') > -1){
        alert('; found in NCBI ID list, please use a plain comma (,) to separate IDs');
        return false;
    }

    if (ncbi.indexOf(' ') > -1 || ncbi.indexOf('\t') > -1){
        alert('whitespace found in NCBI ID list, please use a comma (,) to separate IDs');
        return false;
    }
    return true;
}

function update_status(url) {
    $.getJSON(url, function(json) {
        $("#server-status").html(json.status);
        $("#queue-length").html(json.queue_length);
        $("#running-jobs").html(json.running);
        $("#total-jobs").html(json.total_jobs);
        if(json.ts_queued_m == null){
            $("#queue-details").hide();
        } else {
            $("#queue-time").attr("datetime", json.ts_queued_m);
            $("#queue-time").text($.timeago(json.ts_queued_m));
            $("#queue-details").show();
        }
        $("#long-runtime").html(json.long_running);
        if(json.ts_timeconsuming_m == null){
            $("#long-queue-details").hide();
        } else {
            $("#long-queue-time").attr("datetime", json.ts_timeconsuming_m);
            $("#long-queue-time").text($.timeago(json.ts_timeconsuming_m));
            $("#long-queue-details").show();
        }
    });
}

function repeatedly_update_status(url) {
    update_status(url);
    $.timer(10000, function(timer) {
        update_status(url);
    });
}

function display_notices(url, more_url) {
    $.getJSON(url, function(json) {
        if (json.notices.length < 1) {
            return;
        }
        for (var n in json.notices) {
            var notice_data = json.notices[n];
            var add_more_link = false;
            var cutoff = 100;

            var notice = $('<div>');
            notice.addClass('alert alert-block');
            notice.addClass('alert-' + notice_data.category);
            notice.append('<a href="#" class="close" data-dismiss="alert">&times;</a>');
            var teaser = $('<h4>');
            teaser.text(notice_data.teaser);
            notice.append(teaser);
            var contents = $('<div>');
            if ( more_url !== undefined && notice_data.category != "error") {
                if (notice_data.text.length > cutoff) {
                    var last_space = notice_data.text.lastIndexOf(' ', cutoff);
                    cutoff = last_space > 10 ? last_space : cutoff;
                    notice_data.text = notice_data.text.substr(0, cutoff);
                    add_more_link = true;
                }
            }
            contents.text(notice_data.text);
            contents.html(contents.html().replace(/\n/g,'<br>'));
            notice.append(contents);

            if ( add_more_link ) {
                var more = $('<a>');
                more.attr('href', more_url + "#" + notice_data.id);
                more.text('...more...');
                notice.append(more);
            }

            if (notice_data.category == "error") {
                $('#error-container').append(notice);
            } else {
                $('#notice-container').append(notice);
            }

        }
    });
}

function display_job_status(url, img_dir) {
    $.getJSON(url, function(json) {
        $('body').data('job_status', json.short_status);
        $("#last-changed").text(json.last_changed.replace(/\..*/g, ''));
        var stat = json.status;
        stat = stat.replace(/\n/g, '<br>');
        $("#status").html(stat);
        $("#status-img").attr('src', img_dir + '/' + json.short_status + '.gif');
        if (json.status != 'done') {
            return;
        }
        var result = $('<a>');
        result.attr('href', json.result_url);
        result.text('result');
        $('#result-link').append('See the ');
        $('#result-link').append(result);
        $.timer(5000, function(timer) {
            window.location.href = json.result_url;
        });
    });
}

function repeatedly_update_job_status(url, img_dir) {
    $.timer(10000, function(timer) {
        display_job_status(url, img_dir);
        var stat = $('body').data('job_status');
        if ( stat == 'done' || stat == 'failed' ) {
            timer.stop();
        }
    });
}
