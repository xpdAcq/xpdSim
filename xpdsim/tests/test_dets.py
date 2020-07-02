import pytest
import numpy as np
from pathlib import Path
from cycler import cycler
from numpy.testing import assert_array_equal

import bluesky.plans as bp
import bluesky.plan_stubs as bs
from ophyd import sim

from tifffile import imread

from xpdsim.area_det import (
    XPD_SHUTTER_CONF,
    nsls_ii_path,
    chess_path,
    det_factory,
    build_image_cycle,
    img_gen,
    add_fake_cam,
    PE_IMG_SIZE,
    DEXELA_IMG_SIZE,
    BLACKFLY_IMG_SIZE

)
from xpdsim.movers import shctl1

test_params = [("nslsii", nsls_ii_path), ("chess", chess_path)]


@pytest.mark.parametrize(("name", "fp"), test_params)
def test_img_shape(name, fp):
    p = Path(fp)
    shape_check = [
        imread(str(fp)).shape == PE_IMG_SIZE for fp in p.glob("*.tif*")
    ]
    assert all(shape_check)


def test_add_cam():
    device = sim.SynSignalWithRegistry(name='yolo')
    det = add_fake_cam(device)
    assert hasattr(det, 'images_per_set')
    assert hasattr(det, 'number_of_sets')
    assert hasattr(det, 'cam')
    assert hasattr(det.cam, 'acquire_time')
    assert hasattr(det.cam, 'acquire')


@pytest.mark.parametrize(("name", "fp"), test_params)
def test_dets(RE, db, fp, name):
    det = det_factory(build_image_cycle(fp))
    RE.subscribe(db.insert, "all")
    uid = RE(bp.count([det]))
    cycle2 = build_image_cycle(fp)
    cg = cycle2()
    for name, doc in db.restream(db[-1], fill=True):
        if name == "event":
            db_img = doc["data"]["pe1_image"]
            cycler_img = next(cg)["pe1_image"]
            assert_array_equal(db_img, cycler_img)
            assert db_img.squeeze().shape == PE_IMG_SIZE
            assert cycler_img.squeeze().shape == PE_IMG_SIZE
    assert uid is not None


@pytest.mark.parametrize(("name", "fp"), test_params)
def test_dets_shutter(RE, db, name, fp):
    det = det_factory(cycle=build_image_cycle(fp),
                      shutter=shctl1)
    RE.subscribe(db.insert, "all")
    uid = RE(bp.count([det]))
    cycle2 = build_image_cycle(fp)
    cg = cycle2()
    # With the shutter down
    RE(bs.abs_set(shctl1, XPD_SHUTTER_CONF["close"], wait=True))
    uid = RE(bp.count([det]))
    for name, doc in db.restream(db[-1], fill=True):
        if name == "event":
            assert_array_equal(
                doc["data"]["pe1_image"],
                np.zeros_like(doc["data"]["pe1_image"]),
            )
    assert uid is not None

    # With the shutter up
    RE(bs.abs_set(shctl1, XPD_SHUTTER_CONF["open"], wait=True))
    print('outside shutter id =', id(shctl1))
    print('outside shutter status =', shctl1.get())
    uid = RE(bp.count([det]))
    for name, doc in db.restream(db[-1], fill=True):
        if name == "event":
            assert_array_equal(doc["data"]["pe1_image"],
                               next(cg)["pe1_image"])
    assert uid is not None


@pytest.mark.xfail
@pytest.mark.parametrize(("name", "fp"), test_params)
def test_dets_noise(RE, db, name, fp):
    det = det_factory(
        db.reg, src_path=fp, shutter=shctl1, noise=np.random.poisson
    )
    RE.subscribe(db.insert, "all")
    cycle2 = build_image_cycle(fp)
    cg = cycle2()
    RE(bp.count([det]))
    for name, doc in db.restream(db[-1], fill=True):
        if name == "event":
            assert_array_equal(doc["data"]["pe1_image"], next(cg)["pe1_image"])


@pytest.mark.parametrize(
    ("shutter", "noise"),
    [(x, y) for x in [None, shctl1] for y in [None, np.random.poisson]],
)
def test_dexela(RE, db, shutter, noise):
    print(DEXELA_IMG_SIZE)
    det = det_factory(shutter=shutter,
                      noise=noise,
                      size=DEXELA_IMG_SIZE,
                      data_key='dexela_image')
    RE.subscribe(db.insert, "all")
    RE(bs.abs_set(shctl1, XPD_SHUTTER_CONF["open"], wait=True))
    uid = RE(bp.count([det]))
    for name, doc in db.restream(db[-1], fill=True):
        if name == "event":
            db_img = doc["data"]["dexela_image"]
            assert db_img.squeeze().shape == DEXELA_IMG_SIZE
    assert uid is not None
    if shutter:
        RE(bs.abs_set(shctl1, XPD_SHUTTER_CONF["close"], wait=True))
        uid = RE(bp.count([det]))
        for name, doc in db.restream(db[-1], fill=True):
            if name == "event":
                db_img = doc["data"]["dexela_image"]
                assert db_img.squeeze().shape == DEXELA_IMG_SIZE
                assert np.allclose(db_img, np.zeros_like(db_img))
        assert uid is not None


@pytest.mark.parametrize(
    ("shutter", "noise"),
    [(x, y) for x in [None, shctl1] for y in [None, np.random.poisson]],
)
def test_blackfly(RE, db, shutter, noise):
    for cycle in [None,
                  cycler("blackfly_det_image",
                         [np.ones(BLACKFLY_IMG_SIZE)])]:
        det = det_factory(cycle=cycle,
                          data_key="blackfly_det_image",
                          shutter=shutter,
                          noise=noise,
                          size=BLACKFLY_IMG_SIZE,
                          )
        RE.subscribe(db.insert, "all")
        RE(bs.abs_set(shctl1, XPD_SHUTTER_CONF["open"], wait=True))
        uid = RE(bp.count([det]))
        for name, doc in db.restream(db[-1], fill=True):
            if name == "event":
                db_img = doc["data"]["blackfly_det_image"]
                assert db_img.squeeze().shape == BLACKFLY_IMG_SIZE
        assert uid is not None
        if shutter:
            RE(bs.abs_set(shctl1, XPD_SHUTTER_CONF["close"], wait=True))
            uid = RE(bp.count([det]))
            for name, doc in db.restream(db[-1], fill=True):
                if name == "event":
                    db_img = doc["data"]["blackfly_det_image"]
                    assert db_img.squeeze().shape == BLACKFLY_IMG_SIZE
                    assert np.allclose(db_img, np.zeros_like(db_img))
            assert uid is not None
