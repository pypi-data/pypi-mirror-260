"""Clusters subcommands."""

from typing import List, Optional

import typer
from rich.panel import Panel
from rich.table import Table

from cyberfusion.ClusterCli._utilities import (
    BOOL_MESSAGE,
    CONFIRM_MESSAGE,
    DETAILED_MESSAGE,
    EMTPY_TO_CLEAR_MESSAGE,
    RANDOM_PASSWORD_MESSAGE,
    catch_api_exception,
    console,
    delete_api_object,
    exit_with_status,
    get_object,
    get_support,
    get_usages_plot,
    get_usages_timestamp,
    handle_manual_error,
    print_warning,
    wait_for_task,
)
from cyberfusion.ClusterSupport import Cluster
from cyberfusion.ClusterSupport.clusters import (
    ClusterGroup,
    HTTPRetryCondition,
    MeilisearchEnvironment,
    PHPExtension,
    UNIXUserHomeDirectory,
)
from cyberfusion.ClusterSupport.enums import IPAddressFamily
from cyberfusion.Common import generate_random_string

app = typer.Typer()

HELP_PANEL_SHOW = "Show cluster"
HELP_PANEL_UPDATE = "Update cluster"
HELP_PANEL_IP_ADDRESSES = "IP addresses"

ERROR_MISSING_HTTP_RETRY_PROPERTIES = "Cluster does not have HTTP retry properties. This usually means the cluster does not have compatible groups."


@app.command("list")
@catch_api_exception
def list_(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)
) -> None:
    """List clusters."""
    console.print(
        get_support().get_table(objs=get_support().clusters, detailed=detailed)
    )


@app.command(rich_help_panel=HELP_PANEL_SHOW)
@catch_api_exception
def get(
    name: str,
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE),
) -> None:
    """Show cluster."""
    console.print(
        get_support().get_table(
            objs=[get_object(get_support().clusters, name=name)],
            detailed=detailed,
        )
    )


@app.command(rich_help_panel=HELP_PANEL_SHOW)
@catch_api_exception
def get_borg_ssh_key(
    name: str,
) -> None:
    """Show Borg SSH key."""
    cluster = get_object(get_support().clusters, name=name)

    console.print(cluster.get_borg_public_ssh_key())


@app.command()
@catch_api_exception
def create(
    customer_team_code: Optional[str] = typer.Option(
        default=None, help="Do not set unless superuser"
    ),
    groups: List[ClusterGroup] = typer.Option(
        [], "--group", show_default=False
    ),
    description: str = typer.Option(default=...),
    site_name: str = typer.Option(default=...),
    kernelcare_license_key: Optional[str] = typer.Option(default=None),
    unix_users_home_directory: Optional[UNIXUserHomeDirectory] = typer.Option(
        default=None, help="Groups: Web, Mail, Borg Server", show_default=False
    ),
    sync_toolkit_enabled: bool = typer.Option(
        False, "--with-sync-toolkit", help="Groups: Web, Database"
    ),
    php_versions: List[str] = typer.Option(
        default=[], rich_help_panel="Group: Web"
    ),
    custom_php_modules_names: List[PHPExtension] = typer.Option(
        default=[], rich_help_panel="Group: Web"
    ),
    php_ioncube_enabled: bool = typer.Option(
        False, "--with-php-ioncube", rich_help_panel="Group: Web"
    ),
    php_sessions_spread_enabled: bool = typer.Option(
        False, "--with-php-sessions-spread", rich_help_panel="Group: Web"
    ),
    nodejs_version: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Web"
    ),
    nodejs_versions: List[str] = typer.Option(
        default=[], rich_help_panel="Group: Web"
    ),
    wordpress_toolkit_enabled: bool = typer.Option(
        False, "--with-wordpress-toolkit", rich_help_panel="Group: Web"
    ),
    bubblewrap_toolkit_enabled: bool = typer.Option(
        False, "--with-bubblewrap-toolkit", rich_help_panel="Group: Web"
    ),
    mariadb_version: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    mariadb_cluster_name: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    mariadb_backup_interval: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    postgresql_version: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    postgresql_backup_interval: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    redis_password: Optional[str] = typer.Option(
        default=generate_random_string,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
        rich_help_panel="Group: Database",
    ),
    redis_memory_limit: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    database_toolkit_enabled: bool = typer.Option(
        False, "--with-database-toolkit", rich_help_panel="Group: Database"
    ),
    automatic_borg_repositories_prune_enabled: bool = typer.Option(
        False,
        "--with-automatic-borg-repositories-prune",
        rich_help_panel="Group: Borg Client",
    ),
    grafana_domain: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    singlestore_studio_domain: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    singlestore_api_domain: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    singlestore_license_key: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    singlestore_root_password: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    metabase_domain: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    metabase_database_password: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    kibana_domain: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    rabbitmq_management_domain: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    rabbitmq_admin_password: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    rabbitmq_erlang_cookie: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    new_relic_mariadb_password: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    new_relic_apm_license_key: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    new_relic_infrastructure_license_key: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    mariadb_backup_local_retention: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    postgresql_backup_local_retention: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    meilisearch_backup_local_retention: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    elasticsearch_default_users_password: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    meilisearch_master_key: Optional[str] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    meilisearch_backup_interval: Optional[int] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    meilisearch_environment: Optional[MeilisearchEnvironment] = typer.Option(
        default=None, rich_help_panel="Group: Database"
    ),
    automatic_upgrades_enabled: bool = False,
    firewall_rules_external_providers_enabled: bool = False,
) -> None:
    """Create cluster."""
    cluster = Cluster(get_support())

    site = get_object(get_support().sites, name=site_name)

    if customer_team_code:
        if not get_support().is_superuser:
            handle_manual_error(
                "Customer team code must be unset when not superuser"
            )

        customer_id = get_object(
            get_support().customers, team_code=customer_team_code
        ).id
    else:
        if get_support().is_superuser:
            handle_manual_error(
                "Customer team code must be set when superuser"
            )

        customer_id = get_support().customer_id

    if ClusterGroup.DB not in groups:
        redis_password = None  # Reset default value

    task_collection = cluster.create(
        customer_id=customer_id,
        site_id=site.id,
        groups=groups,
        description=description,
        kernelcare_license_key=kernelcare_license_key,
        unix_users_home_directory=unix_users_home_directory,
        sync_toolkit_enabled=sync_toolkit_enabled,
        php_versions=php_versions,
        custom_php_modules_names=custom_php_modules_names,
        php_ioncube_enabled=php_ioncube_enabled,
        php_sessions_spread_enabled=php_sessions_spread_enabled,
        nodejs_version=nodejs_version,
        nodejs_versions=nodejs_versions,
        wordpress_toolkit_enabled=wordpress_toolkit_enabled,
        bubblewrap_toolkit_enabled=bubblewrap_toolkit_enabled,
        mariadb_version=mariadb_version,
        mariadb_cluster_name=mariadb_cluster_name,
        mariadb_backup_interval=mariadb_backup_interval,
        postgresql_version=postgresql_version,
        postgresql_backup_interval=postgresql_backup_interval,
        grafana_domain=grafana_domain,
        singlestore_studio_domain=singlestore_studio_domain,
        singlestore_api_domain=singlestore_api_domain,
        singlestore_license_key=singlestore_license_key,
        singlestore_root_password=singlestore_root_password,
        metabase_domain=metabase_domain,
        metabase_database_password=metabase_database_password,
        kibana_domain=kibana_domain,
        rabbitmq_management_domain=rabbitmq_management_domain,
        rabbitmq_admin_password=rabbitmq_admin_password,
        rabbitmq_erlang_cookie=rabbitmq_erlang_cookie,
        automatic_upgrades_enabled=automatic_upgrades_enabled,
        firewall_rules_external_providers_enabled=firewall_rules_external_providers_enabled,
        new_relic_mariadb_password=new_relic_mariadb_password,
        new_relic_apm_license_key=new_relic_apm_license_key,
        new_relic_infrastructure_license_key=new_relic_infrastructure_license_key,
        mariadb_backup_local_retention=mariadb_backup_local_retention,
        postgresql_backup_local_retention=postgresql_backup_local_retention,
        meilisearch_backup_local_retention=meilisearch_backup_local_retention,
        elasticsearch_default_users_password=elasticsearch_default_users_password,
        redis_password=redis_password,
        redis_memory_limit=redis_memory_limit,
        database_toolkit_enabled=database_toolkit_enabled,
        automatic_borg_repositories_prune_enabled=automatic_borg_repositories_prune_enabled,
        http_retry_properties=None,
        meilisearch_master_key=meilisearch_master_key,
        meilisearch_backup_interval=meilisearch_backup_interval,
        meilisearch_environment=meilisearch_environment,
        php_settings={},
    )

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def add_groups(name: str, groups: List[ClusterGroup]) -> None:
    """Add groups."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.groups.extend(groups)
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_description(name: str, description: str) -> None:
    """Update description."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.description = description
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_kernelcare_license_key(
    name: str,
    kernelcare_license_key: Optional[str] = typer.Argument(
        default=..., help=EMTPY_TO_CLEAR_MESSAGE
    ),
) -> None:
    """Update KernelCare license key."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.kernelcare_license_key = kernelcare_license_key
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def add_php_versions(name: str, php_versions: List[str]) -> None:
    """Add PHP versions."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.php_versions.extend(php_versions)
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
@exit_with_status
def remove_php_versions(name: str, php_versions: List[str]) -> int:
    """Remove PHP versions."""
    cluster = get_object(get_support().clusters, name=name)

    exit_code = 0
    success = False

    for php_version in php_versions:
        try:
            cluster.php_versions.remove(php_version)
            success = True
        except ValueError:
            print_warning(f"PHP version '{php_version}' not found, skipping.")
            exit_code = 64

    if not success:
        handle_manual_error("No PHP versions have been removed")

    cluster.update()

    return exit_code


@app.command(rich_help_panel=HELP_PANEL_SHOW)
@catch_api_exception
def get_php_settings(
    name: str,
) -> None:
    """Get PHP settings."""
    cluster = get_object(get_support().clusters, name=name)

    table = Table(
        expand=True,
        show_lines=False,
        show_edge=False,
        box=None,
        show_header=False,
    )

    for key, value in cluster.php_settings.items():
        table.add_row(key, str(value))

    console.print(Panel(table, title="PHP Settings", title_align="left"))


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_php_setting(name: str, key: str, value: str) -> None:
    """Update PHP setting."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.php_settings[key] = value
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_http_retry_tries_failover_amount(
    name: str, tries_failover_amount: int
) -> None:
    """Update HTTP retry tries failover amount."""
    cluster = get_object(get_support().clusters, name=name)

    if not cluster.http_retry_properties:
        handle_manual_error(ERROR_MISSING_HTTP_RETRY_PROPERTIES)

    cluster.http_retry_properties["tries_failover_amount"] = (
        tries_failover_amount
    )

    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_http_retry_tries_amount(name: str, tries_amount: int) -> None:
    """Update HTTP retry tries amount.

    If no conditions are set yet, sane defaults are set.
    """
    cluster = get_object(get_support().clusters, name=name)

    if not cluster.http_retry_properties:
        handle_manual_error(ERROR_MISSING_HTTP_RETRY_PROPERTIES)

    cluster.http_retry_properties["tries_amount"] = tries_amount

    if not cluster.http_retry_properties[
        "conditions"
    ]:  # Can't set tries_amount without conditions
        cluster.http_retry_properties["conditions"] = [
            HTTPRetryCondition.CONNECTION_FAILURE,
            HTTPRetryCondition.EMPTY_RESPONSE,
            HTTPRetryCondition.JUNK_RESPONSE,
            HTTPRetryCondition.RESPONSE_TIMEOUT,
            HTTPRetryCondition.ZERO_RTT_REJECTED,
            HTTPRetryCondition.HTTP_STATUS_500,
            HTTPRetryCondition.HTTP_STATUS_502,
            HTTPRetryCondition.HTTP_STATUS_503,
            HTTPRetryCondition.HTTP_STATUS_504,
        ]

    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def add_http_retry_conditions(
    name: str, conditions: List[HTTPRetryCondition]
) -> None:
    """Add NodeJS versions."""
    cluster = get_object(get_support().clusters, name=name)

    if not cluster.http_retry_properties:
        handle_manual_error(ERROR_MISSING_HTTP_RETRY_PROPERTIES)

    cluster.http_retry_properties["conditions"].extend(conditions)
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
@exit_with_status
def remove_http_retry_conditions(
    name: str, conditions: List[HTTPRetryCondition]
) -> int:
    """Remove HTTP retry properties conditions."""
    cluster = get_object(get_support().clusters, name=name)

    if not cluster.http_retry_properties:
        handle_manual_error(ERROR_MISSING_HTTP_RETRY_PROPERTIES)

    exit_code = 0
    success = False

    for condition in conditions:
        try:
            cluster.http_retry_properties["conditions"].remove(condition)
            success = True
        except ValueError:
            print_warning(
                f"HTTP retry condition '{condition}' not found, skipping."
            )
            exit_code = 64

    if not success:
        handle_manual_error("No HTTP retry conditions have been removed")

    cluster.update()

    return exit_code


@app.command()
@catch_api_exception
def add_custom_php_modules(
    name: str, custom_php_modules_names: List[PHPExtension]
) -> None:
    """Add custom PHP modules."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.custom_php_modules_names.extend(custom_php_modules_names)
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_php_ioncube(
    name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update PHP ionCube."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.php_ioncube_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_php_session_spread(
    name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update PHP session spread."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.php_sessions_spread_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_nodejs_version(
    name: str,
    nodejs_version: int,
) -> None:
    """Update NodeJS version."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.nodejs_version = nodejs_version
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def add_nodejs_versions(name: str, nodejs_versions: List[str]) -> None:
    """Add NodeJS versions."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.nodejs_versions.extend(nodejs_versions)
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
@exit_with_status
def remove_nodejs_versions(name: str, nodejs_versions: List[str]) -> int:
    """Remove NodeJS versions."""
    cluster = get_object(get_support().clusters, name=name)

    exit_code = 0
    success = False

    for nodejs_version in nodejs_versions:
        try:
            cluster.nodejs_versions.remove(nodejs_version)
            success = True
        except ValueError:
            print_warning(
                f"NodeJS version '{nodejs_version}' not found, skipping."
            )
            exit_code = 64

    if not success:
        handle_manual_error("No NodeJS versions have been removed")

    cluster.update()

    return exit_code


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_wordpress_toolkit(
    name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update WordPress toolkit."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.wordpress_toolkit_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_automatic_borg_repositories_prune(
    name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update automatic Borg repositories prune."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.automatic_borg_repositories_prune_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_sync_toolkit(
    name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update sync toolkit."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.sync_toolkit_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_bubblewrap_toolkit(
    name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update Bubblewrap toolkit."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.bubblewrap_toolkit_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_mariadb_version(
    name: str,
    mariadb_version: str,
) -> None:
    """Update MariaDB version."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.mariadb_version = mariadb_version
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_mariadb_cluster_name(
    name: str,
    mariadb_cluster_name: Optional[str] = typer.Argument(
        default=..., help=EMTPY_TO_CLEAR_MESSAGE
    ),
) -> None:
    """Update MariaDB cluster name."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.mariadb_cluster_name = mariadb_cluster_name
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_mariadb_backup_interval(
    name: str,
    mariadb_backup_interval: int,
) -> None:
    """Update MariaDB backup interval."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.mariadb_backup_interval = mariadb_backup_interval
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_postgresql_version(
    name: str,
    postgresql_version: str,
) -> None:
    """Update PostgreSQL version."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.postgresql_version = postgresql_version
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_postgresql_backup_interval(
    name: str,
    postgresql_backup_interval: int,
) -> None:
    """Update PostgreSQL backup interval."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.postgresql_backup_interval = postgresql_backup_interval
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_redis_memory_limit(
    name: str,
    redis_memory_limit: int,
) -> None:
    """Update Redis memory limit."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.redis_memory_limit = redis_memory_limit
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_redis_password(
    name: str,
    password: str = typer.Option(
        default=generate_random_string,
        prompt=True,
        hide_input=True,
        show_default=False,
        help=RANDOM_PASSWORD_MESSAGE,
    ),
) -> None:
    """Update Redis password."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.redis_password = password
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_database_toolkit(
    name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update database toolkit."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.database_toolkit_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_grafana_domain(
    name: str,
    grafana_domain: str,
) -> None:
    """Update Grafana domain."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.grafana_domain = grafana_domain
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_singlestore_studio_domain(
    name: str,
    singlestore_studio_domain: str,
) -> None:
    """Update SingleStore studio domain."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.singlestore_studio_domain = singlestore_studio_domain
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_singlestore_api_domain(
    name: str,
    singlestore_api_domain: str,
) -> None:
    """Update SingleStore API domain."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.singlestore_api_domain = singlestore_api_domain
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_singlestore_license_key(
    name: str,
    singlestore_license_key: str,
) -> None:
    """Update SingleStore license key."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.singlestore_license_key = singlestore_license_key
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_singlestore_root_password(
    name: str,
    singlestore_root_password: str,
) -> None:
    """Update SingleStore root password."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.singlestore_root_password = singlestore_root_password
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_metabase_domain(
    name: str,
    metabase_domain: str,
) -> None:
    """Update Metabase domain."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.metabase_domain = metabase_domain
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_metabase_database_password(
    name: str,
    metabase_database_password: str,
) -> None:
    """Update Metabase database password."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.metabase_database_password = metabase_database_password
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_kibana_domain(
    name: str,
    kibana_domain: str,
) -> None:
    """Update Kibana domain."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.kibana_domain = kibana_domain
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_rabbitmq_management_domain(
    name: str,
    rabbitmq_management_domain: str,
) -> None:
    """Update RabbitMQ management domain."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.rabbitmq_management_domain = rabbitmq_management_domain
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_rabbitmq_admin_password(
    name: str,
    rabbitmq_admin_password: str,
) -> None:
    """Update RabbitMQ admin password."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.rabbitmq_admin_password = rabbitmq_admin_password
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_rabbitmq_erlang_cookie(
    name: str,
    rabbitmq_erlang_cookie: str,
) -> None:
    """Update RabbitMQ Erlang cookie."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.rabbitmq_erlang_cookie = rabbitmq_erlang_cookie
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_new_relic_mariadb_password(
    name: str,
    new_relic_mariadb_password: str,
) -> None:
    """Update New Relic MariaDB password."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.new_relic_mariadb_password = new_relic_mariadb_password
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_new_relic_apm_license_key(
    name: str,
    new_relic_apm_license_key: str,
) -> None:
    """Update New Relic APM license key."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.new_relic_apm_license_key = new_relic_apm_license_key
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_new_relic_infrastructure_license_key(
    name: str,
    new_relic_infrastructure_license_key: str,
) -> None:
    """Update New Relic infrastructure license key."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.new_relic_infrastructure_license_key = (
        new_relic_infrastructure_license_key
    )
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_mariadb_backup_local_retention(
    name: str,
    mariadb_backup_local_retention: int,
) -> None:
    """Update MariaDB backup local retention."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.mariadb_backup_local_retention = mariadb_backup_local_retention
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_postgresql_backup_local_retention(
    name: str,
    postgresql_backup_local_retention: int,
) -> None:
    """Update PostgreSQL backup local retention."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.postgresql_backup_local_retention = (
        postgresql_backup_local_retention
    )
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_meilisearch_backup_local_retention(
    name: str,
    meilisearch_backup_local_retention: int,
) -> None:
    """Update Meilisearch backup local retention."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.meilisearch_backup_local_retention = (
        meilisearch_backup_local_retention
    )
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_elasticsearch_default_users_password(
    name: str,
    elasticsearch_default_users_password: str,
) -> None:
    """Update Elasticearch default users password."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.elasticsearch_default_users_password = (
        elasticsearch_default_users_password
    )
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_automatic_upgrades(
    name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update automatic upgrades."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.automatic_upgrades_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_firewall_rules_external_providers(
    name: str,
    state: bool = typer.Argument(default=..., help=BOOL_MESSAGE),
) -> None:
    """Update firewall rules external providers."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.firewall_rules_external_providers_enabled = state
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_meilisearch_master_key(
    name: str,
    meilisearch_master_key: str,
) -> None:
    """Update Meilisearch master key."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.meilisearch_master_key = meilisearch_master_key
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_meilisearch_environment(
    name: str,
    meilisearch_environment: MeilisearchEnvironment,
) -> None:
    """Update Meilisearch environment."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.meilisearch_environment = meilisearch_environment
    cluster.update()


@app.command(rich_help_panel=HELP_PANEL_UPDATE)
@catch_api_exception
def update_meilisearch_backup_interval(
    name: str,
    meilisearch_backup_interval: int,
) -> None:
    """Update Meilisearch backup interval."""
    cluster = get_object(get_support().clusters, name=name)

    cluster.meilisearch_backup_interval = meilisearch_backup_interval
    cluster.update()


@app.command()
@catch_api_exception
def delete(
    name: str,
    confirm: bool = typer.Option(
        default=False,
        help=CONFIRM_MESSAGE,
    ),
) -> None:
    """Delete cluster."""
    cluster = get_object(get_support().clusters, name=name)

    delete_api_object(obj=cluster, confirm=confirm)


@app.command(rich_help_panel=HELP_PANEL_SHOW)
@catch_api_exception
def unix_users_home_directories_usages(
    name: str,
    hours_before: Optional[int] = None,
    days_before: Optional[int] = None,
    # Typer has a bug where show_default can't be a string in typer.Option
    # https://github.com/tiangolo/typer/issues/158
    amount: Optional[int] = typer.Option(default=None, show_default="All"),  # type: ignore[call-overload]
) -> None:
    """Show UNIX users home directory usages.

    Using --hours-before OR --days-before is required.
    """
    cluster = get_object(get_support().clusters, name=name)

    timestamp, time_unit = get_usages_timestamp(
        days_before=days_before, hours_before=hours_before
    )

    usages = get_support().unix_users_home_directory_usages(
        cluster_id=cluster.id, timestamp=timestamp, time_unit=time_unit
    )[:amount]

    typer.echo(get_usages_plot(usages=usages))


@app.command()
@catch_api_exception
def get_common_properties() -> None:
    """Get clusters common properties."""
    cluster = Cluster(get_support())

    groups = {
        "IMAP": {
            "imap_hostname": "Hostname",
            "imap_port": "Port",
            "imap_encryption": "Encryption",
        },
        "POP3": {
            "pop3_hostname": "Hostname",
            "pop3_port": "Port",
            "pop3_encryption": "Encryption",
        },
        "SMTP": {
            "smtp_hostname": "Hostname",
            "smtp_port": "Port",
            "smtp_encryption": "Encryption",
        },
        "Databases": {"phpmyadmin_url": "phpMyAdmin URL"},
    }

    properties = cluster.get_common_properties()
    matched_properties = []

    for group in groups:
        table = Table(
            expand=True,
            show_lines=False,
            show_edge=False,
            box=None,
            show_header=False,
        )

        for key in groups[group]:
            table.add_row(groups[group][key], str(properties[key]))
            matched_properties.append(key)

        console.print(Panel(table, title=group, title_align="left"))

    unmatched_properties = [
        k for k in properties.keys() if k not in matched_properties
    ]

    if len(unmatched_properties) > 0:
        table = Table(
            expand=True,
            show_lines=False,
            show_edge=False,
            box=None,
            show_header=False,
        )

        for key in unmatched_properties:
            table.add_row(key, str(properties[key]))

        console.print(Panel(table, title="Other", title_align="left"))


@app.command(rich_help_panel=HELP_PANEL_IP_ADDRESSES)
@catch_api_exception
def list_ip_addresses_products(
    detailed: bool = typer.Option(default=False, help=DETAILED_MESSAGE)
) -> None:
    """List IP addresses products."""
    console.print(
        get_support().get_table(
            objs=get_support().cluster_ip_addresses_products, detailed=detailed
        )
    )


@app.command(rich_help_panel=HELP_PANEL_IP_ADDRESSES)
@catch_api_exception
def list_ip_addresses(name: str) -> None:
    """List IP addresses."""
    cluster = get_object(get_support().clusters, name=name)

    ip_addresses = cluster.get_ip_addresses()

    table = Table(
        expand=True,
        show_lines=False,
        show_edge=False,
        box=None,
    )

    for column in [
        "Service Account Group",
        "Service Account Name",
        "IP Address",
        "DNS Name",
        "Default",
    ]:
        table.add_column(column, overflow="fold")

    for service_account_group, service_accounts in ip_addresses.items():
        for service_account_name, ip_addresses in service_accounts.items():
            for ip_address in ip_addresses:
                table.add_row(
                    service_account_group,
                    service_account_name,
                    ip_address["ip_address"],
                    ip_address["dns_name"],
                    str(not ip_address["dns_name"]),
                )

    console.print(Panel(table, title="IP Addresses", title_align="left"))


@app.command(rich_help_panel=HELP_PANEL_IP_ADDRESSES)
@catch_api_exception
def create_ip_address(
    name: str,
    service_account_name: str,
    dns_name: str,
    address_family: IPAddressFamily,
) -> None:
    """Create IP address."""
    cluster = get_object(get_support().clusters, name=name)

    task_collection = cluster.create_ip_address(
        service_account_name=service_account_name,
        dns_name=dns_name,
        address_family=address_family,
    )

    wait_for_task(task_collection_uuid=task_collection.uuid)


@app.command(rich_help_panel=HELP_PANEL_IP_ADDRESSES)
@catch_api_exception
def delete_ip_address(name: str, ip_address: str) -> None:
    """Delete IP address."""
    cluster = get_object(get_support().clusters, name=name)

    task_collection = cluster.delete_ip_address(ip_address=ip_address)

    wait_for_task(task_collection_uuid=task_collection.uuid)
