from shapely.geometry.base import BaseGeometry

from .morphology import closing, opening

__all__ = ["zero_buffer", "deflimmer", "clean_geometry", "unflimmer", "sanitise"]


def zero_buffer(
    geom: BaseGeometry,
) -> BaseGeometry:
    return geom.buffer(0)


def deflimmer(geom: BaseGeometry, eps: float = 1e-7) -> BaseGeometry:
    """

    :param geom:
    :param eps:
    :return:
    """
    return opening(closing(geom, eps), eps)


clean_geometry = unflimmer = deflimmer


def sanitise(geom: BaseGeometry, *args: callable) -> BaseGeometry:
    """
      #A positive distance produces a dilation, a negative distance an erosion. A very small or zero distance may sometimes be used to “tidy” a polygon.

    :param geom:
    :param args:
    :return:
    """

    if not len(args):
        args = (zero_buffer, deflimmer)

    for f in args:
        geom = f(geom)

    return geom
