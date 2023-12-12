import colorsys
from typing import Any, Literal, Optional, TypeAlias

Color: TypeAlias = str | tuple[float, float, float] | tuple[int, int, int]

CSS4_COLORS = {
	'aliceblue': (0.9411764705882353, 0.9725490196078431, 1.0),
	'antiquewhite': (0.9803921568627451, 0.9215686274509803, 0.8431372549019608),
	'aqua': (0.0, 1.0, 1.0),
	'aquamarine': (0.4980392156862745, 1.0, 0.8313725490196079),
	'azure': (0.9411764705882353, 1.0, 1.0),
	'beige': (0.9607843137254902, 0.9607843137254902, 0.8627450980392157),
	'bisque': (1.0, 0.8941176470588236, 0.7686274509803922),
	'black': (0.0, 0.0, 0.0),
	'blanchedalmond': (1.0, 0.9215686274509803, 0.803921568627451),
	'blue': (0.0, 0.0, 1.0),
	'blueviolet': (0.5411764705882353, 0.16862745098039217, 0.8862745098039215),
	'brown': (0.6470588235294118, 0.16470588235294117, 0.16470588235294117),
	'burlywood': (0.8705882352941177, 0.7215686274509804, 0.5294117647058824),
	'cadetblue': (0.37254901960784315, 0.6196078431372549, 0.6274509803921569),
	'chartreuse': (0.4980392156862745, 1.0, 0.0),
	'chocolate': (0.8235294117647058, 0.4117647058823529, 0.11764705882352941),
	'coral': (1.0, 0.4980392156862745, 0.3137254901960784),
	'cornflowerblue': (0.39215686274509803, 0.5843137254901961, 0.9294117647058824),
	'cornsilk': (1.0, 0.9725490196078431, 0.8627450980392157),
	'crimson': (0.8627450980392157, 0.0784313725490196, 0.23529411764705882),
	'cyan': (0.0, 1.0, 1.0),
	'darkblue': (0.0, 0.0, 0.5450980392156862),
	'darkcyan': (0.0, 0.5450980392156862, 0.5450980392156862),
	'darkgoldenrod': (0.7215686274509804, 0.5254901960784314, 0.043137254901960784),
	'darkgray': (0.6627450980392157, 0.6627450980392157, 0.6627450980392157),
	'darkgreen': (0.0, 0.39215686274509803, 0.0),
	'darkgrey': (0.6627450980392157, 0.6627450980392157, 0.6627450980392157),
	'darkkhaki': (0.7411764705882353, 0.7176470588235294, 0.4196078431372549),
	'darkmagenta': (0.5450980392156862, 0.0, 0.5450980392156862),
	'darkolivegreen': (0.3333333333333333, 0.4196078431372549, 0.1843137254901961),
	'darkorange': (1.0, 0.5490196078431373, 0.0),
	'darkorchid': (0.6, 0.19607843137254902, 0.8),
	'darkred': (0.5450980392156862, 0.0, 0.0),
	'darksalmon': (0.9137254901960784, 0.5882352941176471, 0.47843137254901963),
	'darkseagreen': (0.5607843137254902, 0.7372549019607844, 0.5607843137254902),
	'darkslateblue': (0.2823529411764706, 0.23921568627450981, 0.5450980392156862),
	'darkslategray': (0.1843137254901961, 0.30980392156862746, 0.30980392156862746),
	'darkslategrey': (0.1843137254901961, 0.30980392156862746, 0.30980392156862746),
	'darkturquoise': (0.0, 0.807843137254902, 0.8196078431372549),
	'darkviolet': (0.5803921568627451, 0.0, 0.8274509803921568),
	'deeppink': (1.0, 0.0784313725490196, 0.5764705882352941),
	'deepskyblue': (0.0, 0.7490196078431373, 1.0),
	'dimgray': (0.4117647058823529, 0.4117647058823529, 0.4117647058823529),
	'dimgrey': (0.4117647058823529, 0.4117647058823529, 0.4117647058823529),
	'dodgerblue': (0.11764705882352941, 0.5647058823529412, 1.0),
	'firebrick': (0.6980392156862745, 0.13333333333333333, 0.13333333333333333),
	'floralwhite': (1.0, 0.9803921568627451, 0.9411764705882353),
	'forestgreen': (0.13333333333333333, 0.5450980392156862, 0.13333333333333333),
	'fuchsia': (1.0, 0.0, 1.0),
	'gainsboro': (0.8627450980392157, 0.8627450980392157, 0.8627450980392157),
	'ghostwhite': (0.9725490196078431, 0.9725490196078431, 1.0),
	'gold': (1.0, 0.8431372549019608, 0.0),
	'goldenrod': (0.8549019607843137, 0.6470588235294118, 0.12549019607843137),
	'gray': (0.5019607843137255, 0.5019607843137255, 0.5019607843137255),
	'green': (0.0, 0.5019607843137255, 0.0),
	'greenyellow': (0.6784313725490196, 1.0, 0.1843137254901961),
	'grey': (0.5019607843137255, 0.5019607843137255, 0.5019607843137255),
	'honeydew': (0.9411764705882353, 1.0, 0.9411764705882353),
	'hotpink': (1.0, 0.4117647058823529, 0.7058823529411765),
	'indianred': (0.803921568627451, 0.3607843137254902, 0.3607843137254902),
	'indigo': (0.29411764705882354, 0.0, 0.5098039215686274),
	'ivory': (1.0, 1.0, 0.9411764705882353),
	'khaki': (0.9411764705882353, 0.9019607843137255, 0.5490196078431373),
	'lavender': (0.9019607843137255, 0.9019607843137255, 0.9803921568627451),
	'lavenderblush': (1.0, 0.9411764705882353, 0.9607843137254902),
	'lawngreen': (0.48627450980392156, 0.9882352941176471, 0.0),
	'lemonchiffon': (1.0, 0.9803921568627451, 0.803921568627451),
	'lightblue': (0.6784313725490196, 0.8470588235294118, 0.9019607843137255),
	'lightcoral': (0.9411764705882353, 0.5019607843137255, 0.5019607843137255),
	'lightcyan': (0.8784313725490196, 1.0, 1.0),
	'lightgoldenrodyellow': (0.9803921568627451, 0.9803921568627451, 0.8235294117647058),
	'lightgray': (0.8274509803921568, 0.8274509803921568, 0.8274509803921568),
	'lightgreen': (0.5647058823529412, 0.9333333333333333, 0.5647058823529412),
	'lightgrey': (0.8274509803921568, 0.8274509803921568, 0.8274509803921568),
	'lightpink': (1.0, 0.7137254901960784, 0.7568627450980392),
	'lightsalmon': (1.0, 0.6274509803921569, 0.47843137254901963),
	'lightseagreen': (0.12549019607843137, 0.6980392156862745, 0.6666666666666666),
	'lightskyblue': (0.5294117647058824, 0.807843137254902, 0.9803921568627451),
	'lightslategray': (0.4666666666666667, 0.5333333333333333, 0.6),
	'lightslategrey': (0.4666666666666667, 0.5333333333333333, 0.6),
	'lightsteelblue': (0.6901960784313725, 0.7686274509803922, 0.8705882352941177),
	'lightyellow': (1.0, 1.0, 0.8784313725490196),
	'lime': (0.0, 1.0, 0.0),
	'limegreen': (0.19607843137254902, 0.803921568627451, 0.19607843137254902),
	'linen': (0.9803921568627451, 0.9411764705882353, 0.9019607843137255),
	'magenta': (1.0, 0.0, 1.0),
	'maroon': (0.5019607843137255, 0.0, 0.0),
	'mediumaquamarine': (0.4, 0.803921568627451, 0.6666666666666666),
	'mediumblue': (0.0, 0.0, 0.803921568627451),
	'mediumorchid': (0.7294117647058823, 0.3333333333333333, 0.8274509803921568),
	'mediumpurple': (0.5764705882352941, 0.4392156862745098, 0.8588235294117647),
	'mediumseagreen': (0.23529411764705882, 0.7019607843137254, 0.44313725490196076),
	'mediumslateblue': (0.4823529411764706, 0.40784313725490196, 0.9333333333333333),
	'mediumspringgreen': (0.0, 0.9803921568627451, 0.6039215686274509),
	'mediumturquoise': (0.2823529411764706, 0.8196078431372549, 0.8),
	'mediumvioletred': (0.7803921568627451, 0.08235294117647059, 0.5215686274509804),
	'midnightblue': (0.09803921568627451, 0.09803921568627451, 0.4392156862745098),
	'mintcream': (0.9607843137254902, 1.0, 0.9803921568627451),
	'mistyrose': (1.0, 0.8941176470588236, 0.8823529411764706),
	'moccasin': (1.0, 0.8941176470588236, 0.7098039215686275),
	'navajowhite': (1.0, 0.8705882352941177, 0.6784313725490196),
	'navy': (0.0, 0.0, 0.5019607843137255),
	'oldlace': (0.9921568627450981, 0.9607843137254902, 0.9019607843137255),
	'olive': (0.5019607843137255, 0.5019607843137255, 0.0),
	'olivedrab': (0.4196078431372549, 0.5568627450980392, 0.13725490196078433),
	'orange': (1.0, 0.6470588235294118, 0.0),
	'orangered': (1.0, 0.27058823529411763, 0.0),
	'orchid': (0.8549019607843137, 0.4392156862745098, 0.8392156862745098),
	'palegoldenrod': (0.9333333333333333, 0.9098039215686274, 0.6666666666666666),
	'palegreen': (0.596078431372549, 0.984313725490196, 0.596078431372549),
	'paleturquoise': (0.6862745098039216, 0.9333333333333333, 0.9333333333333333),
	'palevioletred': (0.8588235294117647, 0.4392156862745098, 0.5764705882352941),
	'papayawhip': (1.0, 0.9372549019607843, 0.8352941176470589),
	'peachpuff': (1.0, 0.8549019607843137, 0.7254901960784313),
	'peru': (0.803921568627451, 0.5215686274509804, 0.24705882352941178),
	'pink': (1.0, 0.7529411764705882, 0.796078431372549),
	'plum': (0.8666666666666667, 0.6274509803921569, 0.8666666666666667),
	'powderblue': (0.6901960784313725, 0.8784313725490196, 0.9019607843137255),
	'purple': (0.5019607843137255, 0.0, 0.5019607843137255),
	'rebeccapurple': (0.4, 0.2, 0.6),
	'red': (1.0, 0.0, 0.0),
	'rosybrown': (0.7372549019607844, 0.5607843137254902, 0.5607843137254902),
	'royalblue': (0.2549019607843137, 0.4117647058823529, 0.8823529411764706),
	'saddlebrown': (0.5450980392156862, 0.27058823529411763, 0.07450980392156863),
	'salmon': (0.9803921568627451, 0.5019607843137255, 0.4470588235294118),
	'sandybrown': (0.9568627450980393, 0.6431372549019608, 0.3764705882352941),
	'seagreen': (0.1803921568627451, 0.5450980392156862, 0.3411764705882353),
	'seashell': (1.0, 0.9607843137254902, 0.9333333333333333),
	'sienna': (0.6274509803921569, 0.3215686274509804, 0.17647058823529413),
	'silver': (0.7529411764705882, 0.7529411764705882, 0.7529411764705882),
	'skyblue': (0.5294117647058824, 0.807843137254902, 0.9215686274509803),
	'slateblue': (0.41568627450980394, 0.35294117647058826, 0.803921568627451),
	'slategray': (0.4392156862745098, 0.5019607843137255, 0.5647058823529412),
	'slategrey': (0.4392156862745098, 0.5019607843137255, 0.5647058823529412),
	'snow': (1.0, 0.9803921568627451, 0.9803921568627451),
	'springgreen': (0.0, 1.0, 0.4980392156862745),
	'steelblue': (0.27450980392156865, 0.5098039215686274, 0.7058823529411765),
	'tan': (0.8235294117647058, 0.7058823529411765, 0.5490196078431373),
	'teal': (0.0, 0.5019607843137255, 0.5019607843137255),
	'thistle': (0.8470588235294118, 0.7490196078431373, 0.8470588235294118),
	'tomato': (1.0, 0.38823529411764707, 0.2784313725490196),
	'turquoise': (0.25098039215686274, 0.8784313725490196, 0.8156862745098039),
	'violet': (0.9333333333333333, 0.5098039215686274, 0.9333333333333333),
	'wheat': (0.9607843137254902, 0.8705882352941177, 0.7019607843137254),
	'white': (1.0, 1.0, 1.0),
	'whitesmoke': (0.9607843137254902, 0.9607843137254902, 0.9607843137254902),
	'yellow': (1.0, 1.0, 0.0),
	'yellowgreen': (0.6039215686274509, 0.803921568627451, 0.19607843137254902),
}
"""
A dictionary of color names and their corresponding RGB triples.

Each color name is a key in lowercase, and the associated value is an RGB triple with values in the range [0, 1].

Examples:
    # Get the RGB triple for the color 'aliceblue'
    >>> CSS4_COLORS['aliceblue']
    (0.9411764705882353, 0.9725490196078431, 1.0)

    # Get the RGB triple for the color 'antiquewhite'
    >>> CSS4_COLORS['antiquewhite']
    (0.9803921568627451, 0.9215686274509803, 0.8431372549019608)
"""


def lerp(x0:Any, x1:Any, t:float) -> Any:
    x1 = x1 if x1 is not None else x0
    if isinstance(x0, (tuple, list)):
        return tuple(c0 + t * c1 for c0, c1 in zip(x0, x1))
    else:
        return x0 + t * (x1 - x0)


def convert_to_rgb(color: Color) -> tuple[float, float, float]:
    """Convert color representation to RGB triple with values in the range [0, 1].

    Args:
        color (Color): The color to convert. It can be a hex string, an RGB tuple with values in the range [0, 1], an RGB tuple with integer values in the range [0, 255], or a standard CSS4 color name.

    Returns:
        Tuple[float, float, float]: The RGB representation of the color in the range [0, 1].

    Raises:
        ValueError: If the color representation is not supported.

    Examples:
        # Convert hex string to RGB
        >>> convert_to_rgb('#FF0000')
        (1.0, 0.0, 0.0)

        # Convert RGB tuple with values in the range [0, 1] to RGB
        >>> convert_to_rgb((0.5, 0.5, 1.0))
        (0.5, 0.5, 1.0)

        # Convert RGB tuple with integer values in the range [0, 255] to RGB
        >>> convert_to_rgb((255, 128, 0))
        (1.0, 0.5019607843137255, 0.0)

        # Convert standard CSS4 color name to RGB
        >>> convert_to_rgb('orange')
        (1.0, 0.6470588235294118, 0.0)
    """
    if isinstance(color, str):  # Assume hex string
        if color[0] == "#":
            return tuple(int(color[i:i + 2], 16) / 255.0 for i in (1, 3, 5))
        elif color.lower() in CSS4_COLORS:
            return CSS4_COLORS[color.lower()]
    elif isinstance(color, tuple):  # Assume RGB tuple
        if all(isinstance(val, int) for val in color):
            return tuple(val / 255.0 for val in color)
        elif all(isinstance(val, float) for val in color):
            return color
    raise ValueError("Unsupported color representation.")


def rgb_to_hex(rgb: tuple[float, float, float]) -> str:
    """
    Convert an RGB triple with float values to a hex string.

    Args:
    	rgb: RGB triple with float values in the range 0 to 1.

    Returns:
   		Hex string representation of the RGB color.
    """
    # Convert float values to integers in the range 0 to 255
    rgb_int = [round(value * 255) for value in rgb]

    # Convert to hex and concatenate
    hex_string = "#{:02X}{:02X}{:02X}".format(*rgb_int)

    return hex_string


def lerp_rgb(c1:tuple[float, float, float], c2:tuple[float, float, float], t:float) -> tuple[float, float, float]:
    """Interpolate colors in the HSV color space.

    This function performs linear interpolation between two colors represented in the Red, Green, Blue (RGB) color model.

    Args:
        c1 (tuple[float, float, float]): The first color in HSV format. Each component should be in the range [0, 1].
        c2 (tuple[float, float, float]): The second color in HSV format. Each component should be in the range [0, 1].
        t (float): Interpolation factor, controlling the blend between the two colors. Should be in the range [0, 1].

    Returns:
        tuple[float, float, float]: The interpolated color in RGB format.

    Raises:
        AssertionError: If any input value is outside the valid range [0, 1].

    Examples:
        # Interpolate between red and blue with a 0.5 blend factor
        >>> lerp_rgb((1.0, 0.0, 0.0), (0.0, 01.0, 1.0), 0.5)
        (0.5, 0.0, 0.5)
    """
    # Validate input ranges
    for rgb in [c1, c2]:
        assert 0 <= rgb[0] <= 1 and 0 <= rgb[1] <= 1 and 0 <= rgb[2] <= 1, "Input values must be in the range [0, 1]."

    r1, g1, b1 = c1
    r2, g2, b2 = c2

    # Interpolate the red, green, and blue components
    r = r1 + (r2 - r1) * t
    g = g1 + (g2 - g1) * t
    b = b1 + (b2 - b1) * t

    return r, g, b


def lerp_hsv(c1:tuple[float, float, float], c2:tuple[float, float, float], t:float, cw: Optional[bool] = None) -> tuple[float, float, float]:
    """Interpolate colors in the HSV color space.

    This function performs linear interpolation between two colors represented in the Hue, Saturation, Value (HSV) color model.

    Args:
        c1 (tuple[float, float, float]): The first color in HSV format. Each component should be in the range [0, 1].
        c2 (tuple[float, float, float]): The second color in HSV format. Each component should be in the range [0, 1].
        t (float): Interpolation factor, controlling the blend between the two colors. Should be in the range [0, 1].
        cw (bool | None, optional): If None, the colors are automatically interpolated along the shortest angular distance.
                                   If True, the hue value is interpolated clockwise; False, counterclockwise.
                                   Defaults to None.

    Returns:
        tuple[float, float, float]: The interpolated color in HSV format.

    Raises:
        AssertionError: If any input value is outside the valid range [0, 1].

    Examples:
        # Interpolate between red and blue with a 0.5 blend factor
        >>> lerp_hsv((0.0, 1.0, 1.0), (0.66, 1.0, 1.0), 0.5)
        (0.833, 1.0, 1.0)

        # Interpolate clockwise between yellow and purple with a 0.25 blend factor
        >>> lerp_hsv((0.16, 1.0, 1.0), (0.75, 1.0, 1.0), 0.25, cw=True)
        (0.663, 1.0, 1.0)
    """
    # Validate input ranges
    for hsv in [c1, c2]:
        assert 0 <= hsv[0] <= 1 and 0 <= hsv[1] <= 1 and 0 <= hsv[2] <= 1, "Input values must be in the range [0, 1]."


    h1, s1, v1 = c1
    h2, s2, v2 = c2

    # Determine the direction of hue interpolation (clockwise or counterclockwise)
    if cw is None:
        cw = (h2 > h1 and h2 - h1 <= 0.5) or (h2 < h1 and 1.0 + h2 - h1 <= 0.5)

    # Adjust hue values for interpolation direction
    h1 = (h1 + 1.0) if not cw and h1 < h2 else h1
    h2 = (h2 + 1.0) if cw and h2 < h1 else h2

    # Interpolate the hue, saturation, and value components
    h = h1 + (h2 - h1) * t
    s = s1 + (s2 - s1) * t
    v = v1 + (v2 - v1) * t

    # Wrap hue back into [0, 1) range
    h = h - 1.0 if h >= 1.0 else h

    return h, s, v


def lerp_color(
    c1: Color,
    c2: Color,
    t:float,
    mode:Literal['rgb', 'hsv']='rgb',
    clockwise:Optional[bool]=None
) -> tuple[float, float, float]:
    """Interpolate colors

    This function performs linear interpolation between two colors. Colors can be represented as a hex string or tuples interpreted as RGB values.

    Args:
        c1 (Union[str, tuple[float, float, float]]): The first color.
        c2 (Union[str, tuple[float, float, float]]): The second color.
        t (float): Interpolation factor, controlling the blend between the two colors. Should be in the range [0, 1].
        mode (Literal['rgb', 'hsv'], optional): The space in which the color will be interpolated. Defaults to 'rgb'.
        clockwise (Optional[bool], optional): If None, the colors are automatically interpolated along the shortest angular distance.
                                   If True, the hue value is interpolated clockwise; False, counterclockwise.
                                   This argument is only used when mode is 'hsv'.
                                   Defaults to None.

    Returns:
        tuple[float, float, float]: The interpolated color in RGB format.

    Examples:
        # Interpolate between red and blue with a 0.5 blend factor using hex strings
        >>> lerp_color('#FF0000', '#0000FF', 0.5)
        (0.5, 0.0, 0.5)

        # Interpolate between red and blue with a 0.5 blend factor using RGB tuples
        >>> lerp_color((1.0, 0.0, 0.0), (0.0, 0.0, 1.0), 0.5)
        (0.5, 0.0, 0.5)

        # Interpolate between red and blue with a 0.5 blend factor in HSV space
        >>> lerp_color((1.0, 0.0, 0.0), '#0000FF', 0.5, mode='hsv')
        (0.5, 0.0, 0.5)
    """

    # Convert color representation to RGB triples with value range 0 to 1
    color_1 = convert_to_rgb(c1)
    color_2 = convert_to_rgb(c2)

    if mode == 'rgb':
        # Perform RGB interpolation
        return lerp_rgb(color_1, color_2, t)
    elif mode == 'hsv':
        c1_hsv = colorsys.rgb_to_hsv(*color_1)
        c2_hsv = colorsys.rgb_to_hsv(*color_2)

        c_hsv = lerp_hsv(c1_hsv, c2_hsv, t, cw=clockwise)

        return colorsys.hsv_to_rgb(*c_hsv)
    else:
        raise ValueError("Invalid mode. Supported modes are 'rgb' and 'hsv'.")