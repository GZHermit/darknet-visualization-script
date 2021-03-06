# coding: utf-8
import re

import app
import filetools
import global_variables as gv

gv._init()


def set_cfg_fp(cfg_fp):
    gv.set_value('cfg_fp', cfg_fp)


def set_data_fp(data_fp):
    gv.set_value('data_fp', data_fp)


def set_gpus(gpus):
    gv.set_value('gpus', gpus)


def set_order(order):
    gv.set_value('order', order)


def set_weight_fp(weight_fp):
    gv.set_value('weight_fp', weight_fp)

def set_video_fp(video_fp):
    gv.set_value('video_fp', video_fp)


def set_draw_option(draw_option):
    gv.set_value('draw_option', draw_option)


def set_valid_step(valid_step):
    gv.set_value('valid_step', valid_step)


def set_compute_step(compute_step):
    gv.set_value('compute_step', compute_step)

def set_thresh(thresh):
    gv.set_value('thresh', thresh)


def show_gv():
    gv_dict = gv.get_all_value()
    print("#------Show the global variables------#")
    for key in gv_dict.keys():
        print("{}:{}".format(key, gv_dict[key]))
    print("#-------------------------------------#")


def set_global_variables():
    args = gv.Args()

    cfg_fp = gv.get_value('cfg_fp')
    data_fp = gv.get_value('data_fp')

    with open(data_fp, 'r') as f:
        options = f.readlines()
        options = [op.strip('\n').split('=') for op in options]
        options = dict(options)

    args.cfg_fn = re.findall('/cfg/(.*?)\.cfg', cfg_fp)[0]
    args.data_fn = re.findall('/cfg/(.*?)\.data', data_fp)[0]
    args.darknet_p = re.findall('(.*)/cfg/', cfg_fp)[0]
    args.gpus = gv.get_value('gpus')
    args.order = gv.get_value('order')
    args.draw_option = gv.get_value('draw_option')
    args.compute_step = gv.get_value('compute_step')
    args.valid_step = gv.get_value('valid_step')
    args.thresh = gv.get_value('thresh')
    key_name = args.data_fn

    train_fn = options['train'].split('/')[-1]
    valid_fn = options['valid'].split('/')[-1]
    cls_fp = options['names']
    result_p = options['results']
    backup_p = options['backup']

    filetools.check_makedir(result_p)
    filetools.check_makedir(backup_p)
    filetools.check_makedir(result_p + '/cache')

    dataset_p = re.sub('/filelist/.*', '', options['train'])

    gv.set_value('key_name', key_name)
    gv.set_value('result_p', result_p)
    gv.set_value('backup_p', backup_p)
    gv.set_value('dataset_p', dataset_p)
    gv.set_value('train_fn', train_fn)
    gv.set_value('valid_fn', valid_fn)
    gv.set_value('cls_fp', cls_fp)

    show_gv()
    return args


def start():
    args = set_global_variables()
    import operations
    if args.order == 'train':
        operations.train(args)
        print("#------train process is over!------#")
    elif args.order == 'valid':
        args.draw_option = 'mAP'
        operations.valid(args)
        operations.compute(args)
        operations.draw(args)
        print("#------valid process is over!------#")
    elif args.order == 'draw':
        operations.draw(args)
    elif args.order == 'compute':
        if args.compute_step is None:
            print("The compute_step cannot be None!")
            exit()
        operations.compute(args)


if __name__ == '__main__':
    app.startApp()
