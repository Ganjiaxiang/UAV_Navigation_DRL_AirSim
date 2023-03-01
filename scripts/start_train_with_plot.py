import sys
import argparse

from PyQt5 import QtWidgets

# from evaluate_td3 import evaluate
# from utils.thread_train import TrainingThread
from utils.thread_train_fixedwing import TrainingThread
from utils.ui_train import TrainingUi
from configparser import ConfigParser


def get_parser():
    parser = argparse.ArgumentParser(
        description="Training navigation model using TD3")
    parser.add_argument('-config', required=True,
                        help='config file name, such as config0925.ini', default='config0925.ini')
    parser.add_argument('-objective', required=True, help='training objective')

    return parser


def main():
    # set config
    # config_file = 'configs/config_NH_SimpleMR_3D.ini'
    config_file = 'configs_new/config_fixedwing.ini'

    # 1. Create the qt thread
    app = QtWidgets.QApplication(sys.argv)
    gui = TrainingUi(config_file)
    gui.show()

    # 2. Start training thread
    training_thread = TrainingThread(config_file)

    training_thread.env.action_signal.connect(gui.action_cb)
    training_thread.env.state_signal.connect(gui.state_cb)
    training_thread.env.attitude_signal.connect(gui.attitude_plot_cb)
    training_thread.env.reward_signal.connect(gui.reward_plot_cb)
    training_thread.env.pose_signal.connect(gui.traj_plot_cb)

    cfg = ConfigParser()
    cfg.read(config_file)
    if cfg.has_option('options', 'perception'):
        if cfg.get('options', 'perception') == 'lgmd':
            training_thread.env.lgmd_signal.connect(gui.lgmd_plot_cb)

    training_thread.start()

    sys.exit(app.exec_())
    print('Exiting program')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('system exit')
