'''
Created on 27/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.print_ import Print

#===================================================================================================
# Run
#===================================================================================================
def Run(params, push=False):
    args = params.args[1:]
    if not args:
        Print('Message for commit is required for git add -A & git commit -m command.')
        return

    from .action_default import Run #@Reimport
    from mu_repo import Params
    Run(Params(params.config, ['add', '-A'], params.config_file))
    Run(Params(params.config, ['commit', '-m', ' '.join(args)], params.config_file))

    if push:
        from mu_repo.action_up import GetReposAndCurrBranch
        from mu_repo.on_output_thread import ExecuteThreadsHandlingOutputQueue
        from mu_repo.execute_git_command_in_thread import ExecuteGitCommandThread
        import Queue

        repos_and_curr_branch = GetReposAndCurrBranch(params)

        threads = []
        output_queue = Queue.Queue()
        for repo, branch in repos_and_curr_branch:
            t = ExecuteGitCommandThread(
                repo, ['push', 'origin', branch], params.config, output_queue)
            threads.append(t)

        ExecuteThreadsHandlingOutputQueue(threads, output_queue, on_output=Print)
