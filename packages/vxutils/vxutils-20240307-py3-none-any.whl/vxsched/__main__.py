"""sched 运行"""

from vxsched import vxsched
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser(description="调度器")
    parser.add_argument("-c", "--config", help="配置文件")
    parser.add_argument("-i", "--mod", help="事件列表")
    args = parser.parse_args()
    vxsched.run()
