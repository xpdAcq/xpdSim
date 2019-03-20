from pathlib import Path

import bluesky.plan_stubs as bs
import bluesky.plans as bp
import numpy as np
import pytest
from numpy.testing import assert_array_equal
from tifffile import imread

from xpdsim.area_det import (
    XPD_SHUTTER_CONF,
    nsls_ii_path,
    chess_path,
    det_factory,
    build_image_cycle,
    det_factory_dexela,
)
from xpdsim.movers import shctl1

test_params = [("nslsii", nsls_ii_path), ("chess", chess_path)]


@pytest.mark.parametrize(("name", "fp"), test_params)
def test_img_shape(name, fp):
    p = Path(fp)
    shape_check = [
        imread(str(fp)).shape == (2048, 2048) for fp in p.glob("*.tif*")
    ]
    assert all(shape_check)


@pytest.mark.parametrize(("name", "fp"), test_params)
def test_dets(RE, db, fp, name):
    det = det_factory(db.reg, src_path=fp)
    RE.subscribe(db.insert, "all")
    uid = RE(bp.count([det]))
    cycle2 = build_image_cycle(fp)
    cg = cycle2()
    for name, doc in db.restream(db[-1], fill=True):
        if name == "event":
            db_img = doc["data"]["pe1_image"]
            cycler_img = next(cg)["pe1_image"]
            assert_array_equal(db_img, cycler_img)
            assert db_img.squeeze().shape == (2048, 2048)
            assert cycler_img.squeeze().shape == (2048, 2048)
    assert uid is not None


@pytest.mark.parametrize(("name", "fp"), test_params)
def test_dets_shutter(RE, db, name, fp):
    det = det_factory(db.reg, src_path=fp, shutter=shctl1)
    RE.subscribe(db.insert, "all")
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
    uid = RE(bp.count([det]))
    for name, doc in db.restream(db[-1], fill=True):
        if name == "event":
            assert_array_equal(doc["data"]["pe1_image"], next(cg)["pe1_image"])
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


def test_dexela(RE, db):
    det = det_factory_dexela(db.reg, shutter=shctl1, noise=np.random.poisson)
    RE.subscribe(db.insert, "all")
    RE(bs.abs_set(shctl1, XPD_SHUTTER_CONF["open"], wait=True))
    uid = RE(bp.count([det]))
    for name, doc in db.restream(db[-1], fill=True):
        if name == "event":
            db_img = doc["data"]["dexela_image"]
            assert db_img.squeeze().shape == (3072, 3888, 0)
    assert uid is not None
    RE(bs.abs_set(shctl1, XPD_SHUTTER_CONF["close"], wait=True))
    uid = RE(bp.count([det]))
    for name, doc in db.restream(db[-1], fill=True):
        if name == "event":
            db_img = doc["data"]["dexela_image"]
            assert db_img.squeeze().shape == (3072, 3888, 0)
            assert np.allclose(db_img, np.zeros_like(db_img))
    assert uid is not None
