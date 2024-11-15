import json
import os

def sabversion():
    return json.loads("""{"version":"4.3.1"}""")

def sabgetconfig(sab_categories):
    config= """
    {
        "config": {
            "misc": {
                "helpful_warnings": 1,
                "queue_complete": "",
                "queue_complete_pers": 0,
                "bandwidth_perc": 100,
                "refresh_rate": 1,
                "interface_settings": "",
                "queue_limit": 20,
                "config_lock": 0,
                "notified_new_skin": 0,
                "check_new_rel": 1,
                "auto_browser": 1,
                "language": "en",
                "enable_https_verification": 1,
                "host": "::",
                "port": 10000,
                "https_port": "",
                "username": "",
                "password": "",
                "bandwidth_max": "",
                "cache_limit": "1G",
                "web_dir": "Glitter",
                "web_color": "Auto",
                "https_cert": "server.cert",
                "https_key": "server.key",
                "https_chain": "",
                "enable_https": 0,
                "inet_exposure": 0,
                "api_key": "(removed)",
                "nzb_key": "(removed)",
                "socks5_proxy_url": "",
                "permissions": "",
                "download_dir": "Downloads/incomplete",
                "download_free": "",
                "complete_dir": "Downloads/complete",
                "complete_free": "",
                "fulldisk_autoresume": 0,
                "script_dir": "",
                "nzb_backup_dir": "",
                "admin_dir": "admin",
                "backup_dir": "",
                "dirscan_dir": "",
                "dirscan_speed": 5,
                "password_file": "",
                "log_dir": "logs",
                "max_art_tries": 3,
                "top_only": 0,
                "sfv_check": 1,
                "script_can_fail": 0,
                "enable_recursive": 1,
                "flat_unpack": 0,
                "par_option": "",
                "pre_check": 0,
                "nice": "",
                "win_process_prio": 3,
                "ionice": "",
                "fail_hopeless_jobs": 1,
                "fast_fail": 1,
                "auto_disconnect": 1,
                "pre_script": "None",
                "end_queue_script": "None",
                "no_dupes": 0,
                "no_series_dupes": 0,
                "no_smart_dupes": 0,
                "dupes_propercheck": 1,
                "pause_on_pwrar": 1,
                "ignore_samples": 0,
                "deobfuscate_final_filenames": 1,
                "auto_sort": "",
                "direct_unpack": 0,
                "propagation_delay": 0,
                "folder_rename": 1,
                "replace_spaces": 0,
                "replace_underscores": 0,
                "replace_dots": 0,
                "safe_postproc": 1,
                "pause_on_post_processing": 0,
                "enable_all_par": 0,
                "sanitize_safe": 0,
                "cleanup_list": [],
                "unwanted_extensions": [],
                "action_on_unwanted_extensions": 0,
                "unwanted_extensions_mode": 0,
                "new_nzb_on_failure": 0,
                "history_retention": "",
                "history_retention_option": "all",
                "history_retention_number": 0,
                "quota_size": "",
                "quota_day": "",
                "quota_resume": 0,
                "quota_period": "m",
                "schedlines": [],
                "rss_rate": 60,
                "ampm": 0,
                "start_paused": 0,
                "preserve_paused_state": 0,
                "enable_par_cleanup": 1,
                "process_unpacked_par2": 1,
                "enable_multipar": 1,
                "enable_unrar": 1,
                "enable_7zip": 1,
                "enable_filejoin": 1,
                "enable_tsjoin": 1,
                "overwrite_files": 0,
                "ignore_unrar_dates": 0,
                "backup_for_duplicates": 0,
                "empty_postproc": 0,
                "wait_for_dfolder": 0,
                "rss_filenames": 0,
                "api_logging": 1,
                "html_login": 1,
                "warn_dupl_jobs": 0,
                "keep_awake": 1,
                "tray_icon": 1,
                "allow_incomplete_nzb": 0,
                "enable_broadcast": 1,
                "ipv6_hosting": 0,
                "ipv6_staging": 0,
                "api_warnings": 1,
                "no_penalties": 0,
                "x_frame_options": 1,
                "allow_old_ssl_tls": 0,
                "enable_season_sorting": 1,
                "verify_xff_header": 0,
                "rss_odd_titles": ["nzbindex.nl/", "nzbindex.com/", "nzbclub.com/"],
                "quick_check_ext_ignore": ["nfo", "sfv", "srr"],
                "req_completion_rate": 100.2,
                "selftest_host": "self-test.sabnzbd.org",
                "movie_rename_limit": "100M",
                "episode_rename_limit": "20M",
                "size_limit": 0,
                "direct_unpack_threads": 3,
                "history_limit": 10,
                "wait_ext_drive": 5,
                "max_foldername_length": 246,
                "nomedia_marker": "",
                "ipv6_servers": 1,
                "url_base": "/sabnzbd",
                "host_whitelist": ["fab0220616e4"],
                "local_ranges": [],
                "max_url_retries": 10,
                "downloader_sleep_time": 10,
                "receive_threads": 2,
                "switchinterval": 0.005,
                "ssdp_broadcast_interval": 15,
                "ext_rename_ignore": [],
                "email_server": "",
                "email_to": [],
                "email_from": "",
                "email_account": "",
                "email_pwd": "",
                "email_endjob": 0,
                "email_full": 0,
                "email_dir": "",
                "email_rss": 0,
                "email_cats": ["*"]
            },
            "logging": {
                "log_level": 1,
                "max_log_size": 5242880,
                "log_backups": 5
            },
            "categories": [
                {"name": "readarr", "order": 1, "pp": "", "script": "Default", "dir": "", "newzbin": "", "priority": -100}
            ]
        }
    }"""
    result = json.loads(config)
    order=0
    for category in sab_categories:
        order = order + 1 
        result["config"]["categories"].append({
            "name": category,
            "order": order,
            "pp": "",
            "script": "Default",
            "dir": "",
            "newzbin": "",
            "priority": -100
        })
    return result
    
def sabgetqueue(downloads):
    slots = []
    index=0
    for download in downloads:
        if download["status"] == "Queued":
            slots.append({
                "index": index,
                "nzo_id": f"SABnzbd_nzo_{download['nzo']}",
                "filename": download['title'],
                "cat": download['cat']
            })
            index = index + 1
    queue="""{"queue":{"version":"4.3.1","paused":false,"pause_int":"0","paused_all":false,"slots":"""
    queue=queue+str(slots)+"}}"
    return queue

def sabgethistory(downloads):
    slots = []
    index=0
    for download in downloads:
        if download["status"] == "Complete":
            slots.append({
                "completed": download['size'],
                "name": download["title"],
                "category": download["cat"],
                "status": "Completed",
                "nzo_id": f"SABnzbd_nzo_{download['nzo']}",
                "storage": download["storage"]
            })
            index = index + 1

    history="""{"history":{"slots":""" + str(slots) + ""","version":"4.3.1"}}"""
    return history

def sabsavequeue(config_dir, downloadqueue):
    with open(os.path.join(config_dir, "sabqueue.conf"),"w") as file:
        json.dump(downloadqueue, file, indent=4)

def sabloadqueue(config_dir):
    if os.path.exists(os.path.join(config_dir, "sabqueue.conf")):
        with open(os.path.join(config_dir, "sabqueue.conf"),"r") as file:
            downloadqueue = json.load(file)
    else:
        downloadqueue = []
    return downloadqueue

def sabdeletefromqueue(config_dir, downloadqueue, item):
    for download in downloadqueue:
        if item == f"SABnzbd_nzo_{download['nzo']}":
            downloadqueue.remove(download)

    with open(os.path.join(config_dir, "sabqueue.conf"),"w") as file:
        json.dump(downloadqueue, file, indent=4)
    return downloadqueue
