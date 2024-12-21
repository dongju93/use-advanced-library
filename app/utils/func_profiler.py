import asyncio
from cProfile import Profile
from functools import wraps
from io import StringIO
from pathlib import Path
from pstats import Stats


def profile_performance(log_file: str = "logs/cprofiler.log"):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)

            profiler = Profile()
            profiler.enable()
            result = await func(*args, **kwargs)
            profiler.disable()

            # StringIO를 사용하여 출력을 캡처
            s = StringIO()
            stats: Stats = (
                Stats(profiler, stream=s).strip_dirs().sort_stats("cumulative")
            )
            stats.print_stats(20)

            # 로그 파일에 기록
            with open(log_file, "a") as f:
                f.write("\n=== Function Profiling Results ===\n")
                f.write(s.getvalue())

            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)

            profiler = Profile()
            profiler.enable()
            result = func(*args, **kwargs)
            profiler.disable()

            # StringIO를 사용하여 출력을 캡처
            s = StringIO()
            stats: Stats = (
                Stats(profiler, stream=s).strip_dirs().sort_stats("cumulative")
            )
            stats.print_stats(20)

            # 로그 파일에 기록
            with open(log_file, "a") as f:
                f.write("\n=== Function Profiling Results ===\n")
                f.write(s.getvalue())

            return result

        return (
            async_wrapper
            if asyncio.iscoroutinefunction(func)
            else sync_wrapper
        )

    return decorator
