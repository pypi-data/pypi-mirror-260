# pylint: disable=too-many-instance-attributes, too-many-arguments, too-many-function-args
"""Local enricher to work with `opendapi enrich` command."""
from typing import Optional
import click

from opendapi.config import OpenDAPIConfig
from opendapi.adapters.dapi_server import (
    DAPIRequests,
    DAPIServerConfig,
    DAPIServerResponse,
)
from opendapi.adapters.file import OpenDAPIFileContents
from opendapi.adapters.git import (
    ChangeTriggerEvent,
    check_if_uncommitted_changes_exist,
    add_all_untracked_files,
)


class Enricher:
    """
    Enrich DAPIs after interacting with the DAPI server.
    Register when appropriate.
    """

    def __init__(
        self,
        config: OpenDAPIConfig,
        dapi_server_config: DAPIServerConfig,
        trigger_event: ChangeTriggerEvent,
        revalidate_all_files: bool = False,
        require_committed_changes: bool = False,
    ) -> None:
        """Initialize the adapter."""
        self.config = config
        self.root_dir = config.root_dir
        self.dapi_server_config = dapi_server_config
        self.trigger_event = trigger_event
        self.revalidate_all_files = revalidate_all_files
        self.require_committed_changes = require_committed_changes

        # Initialize the responses
        self.validate_response: Optional[DAPIServerResponse] = None
        self.register_response: Optional[DAPIServerResponse] = None
        self.analyze_impact_response: Optional[DAPIServerResponse] = None

        self.setup_objects()

    def setup_objects(self):
        """Setup objects in the enricher."""
        self.all_files: OpenDAPIFileContents = self._get_all_files()
        self.changed_files: OpenDAPIFileContents = self._get_changed_files()

        self.dapi_requests = DAPIRequests(
            dapi_server_config=self.dapi_server_config,
            all_files=self.all_files,
            changed_files=self.changed_files,
            error_msg_handler=lambda msg: self.print_markdown_and_text(msg, "red"),
            error_exception_cls=click.ClickException,
            txt_msg_handler=self.print_text_message,
            markdown_msg_handler=self.print_markdown_message,
        )

    def print_markdown_and_text(self, message: str, color: str = "green"):
        """Print errors."""
        self.print_text_message(message, color=color)
        self.print_markdown_message(message)

    @staticmethod
    def print_text_message(message: str, color: str = "green", bold: bool = False):
        """Tell the user something."""
        click.secho(message, fg=color, bold=bold)

    def print_markdown_message(self, message: str):
        """Print a markdown message. Not supported in the CLI."""
        if self.trigger_event.markdown_file:
            with open(
                self.trigger_event.markdown_file, "a", encoding="utf-8"
            ) as markdown_file:
                print(f"{message}\n\n", file=markdown_file)

    def get_base_for_changed_files(self):
        """
        Get the base branch for the changed files.
        Locally, it is the before_change_sha.
        It is overridden in the GithubEnricher.
        """
        return self.trigger_event.before_change_sha

    def _get_all_files(self) -> OpenDAPIFileContents:
        """Get all the OpenDAPI files."""
        return OpenDAPIFileContents.build_from_all_files(self.config)

    def _get_changed_files(self) -> OpenDAPIFileContents:
        """Get the changed OpenDAPI files."""
        if self.revalidate_all_files:
            self.print_markdown_and_text("Tackling all DAPI files", "green")
            return self.all_files
        self.print_markdown_and_text("Tackling only the changed DAPI files", "green")

        # Add all untracked files in case there are any created by `opendapi generate` or the user
        add_all_untracked_files(self.root_dir)
        return self.all_files.filter_changed_files(self.get_base_for_changed_files())

    def _check_if_files_need_to_be_committed(self) -> None:
        """
        Check if the files need to be committed.
        Sometimes, we do not want to overwrite the developer's changes.
        """
        if self.require_committed_changes and check_if_uncommitted_changes_exist(
            self.root_dir
        ):
            raise click.ClickException(
                "Uncommitted changes found. Please commit your changes before running this command"
                " or do not set the `--require-committed-changes` flag. Exiting...",
            )

    def _are_there_files_to_process(self) -> bool:
        """Check if there are files to process."""
        if self.all_files.is_empty:
            self.print_markdown_and_text(
                "No OpenDAPI files found. "
                "Run `opendapi generate` to generate OpenDAPI files.",
                color="yellow",
            )
            return False

        if self.changed_files.is_empty and not self.revalidate_all_files:
            self.print_markdown_and_text(
                "\n\nNo changes to OpenDAPI files found. "
                "\nSet `--revalidate-all-files` if you wish to revalidate all files.",
                color="yellow",
            )
            return False
        return True

    def should_validate(self) -> bool:
        """Check if we should validate the DAPI files."""
        return True

    def should_enrich(self) -> bool:
        """Check if we should enrich the DAPI files."""
        return self.dapi_server_config.suggest_changes

    def print_dapi_server_progress(self, progressbar, progress: int):
        """Print the progress bar for validation."""
        progressbar.update(progress)

    def validate_and_enrich(self) -> DAPIServerResponse:
        """Validate and enrich the DAPI files."""

        self.print_markdown_and_text(
            f"\n\nProcessing {len(self.changed_files.dapis)} DAPI files in"
            f" batch size of {self.dapi_server_config.enrich_batch_size}",
            color="green",
        )
        with click.progressbar(length=len(self.changed_files.dapis)) as progressbar:

            def _notify(progress: int):
                """Notify the user to the progress."""
                return self.print_dapi_server_progress(
                    progressbar, progress
                )  # pragma: no cover

            validate_resp = self.dapi_requests.validate(
                commit_hash=self.trigger_event.after_change_sha,
                suggest_changes_override=self.should_enrich(),
                ignore_suggestions_cache=self.dapi_server_config.ignore_suggestions_cache,
                notify_function=_notify,
            )

        if self.should_enrich():
            self.all_files.update_dapis_with_suggestions(validate_resp.suggestions)

        return validate_resp

    def should_register(self) -> bool:
        """Check if we should register the DAPI files."""
        return False

    def register(self) -> DAPIServerResponse:
        """Register the DAPI files."""
        self.print_markdown_and_text(
            f"\n\nRegistering {len(self.changed_files.dapis)} DAPI files in"
            f" batch size of {self.dapi_server_config.register_batch_size}",
            color="green",
        )
        with click.progressbar(length=len(self.all_files.dapis)) as progressbar:

            def _notify(progress: int):
                """Notify the user to the progress."""
                return self.print_dapi_server_progress(
                    progressbar, progress
                )  # pragma: no cover

            register_resp = self.dapi_requests.register(
                commit_hash=self.trigger_event.after_change_sha,
                source=self.config.urn,
                notify_function=_notify,
            )

            # unregister missing dapis
            self.dapi_requests.unregister(
                source=self.config.urn,
                except_dapi_urns=[
                    dapi["urn"] for dapi in self.all_files.dapis.values()
                ],
            )

            return register_resp

    def should_analyze_impact(self) -> bool:
        """Check if we should analyze the impact."""
        return True

    def post_run_actions(self):
        """Post run actions."""

    def run(self):
        """Run the action."""

        self._check_if_files_need_to_be_committed()

        # Handle no OpenDAPI files or no changes to OpenDAPI files
        if self._are_there_files_to_process():
            # Validate the DAPI files and enrich them if suggestions are enabled
            if self.should_validate():
                self.validate_response = self.validate_and_enrich()

            if self.should_register():
                self.register_response = self.register()

            if self.should_analyze_impact():
                self.analyze_impact_response = self.dapi_requests.analyze_impact()

            self.post_run_actions()

        self.print_markdown_and_text("All done!", "green")
