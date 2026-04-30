import "dart:convert";
import "package:flutter/material.dart";

class JsonUIParser {
  static Map<String, dynamic>? parseSpec(String jsonString) {
    try {
      return jsonDecode(jsonString);
    } catch (e) {
      return null;
    }
  }

  static Color _parseColor(String colorStr) {
    if (colorStr.startsWith("#")) {
      return Color(int.parse("0xFF${colorStr.substring(1)}"));
    }
    return Colors.black;
  }

  static List<Color> _parseColorList(List<dynamic> colors) {
    return colors.map((c) => _parseColor(c.toString())).toList();
  }

  static Widget buildFromJson(Map<String, dynamic> spec) {
    final layout = spec["layout"];
    if (layout == null) return Container();

    final palette = spec["palette"];
    final bgColor = palette != null 
        ? _parseColor(palette["neutrals"][0].toString())
        : const Color(0xFF050816);

    return Container(
      color: bgColor,
      child: _buildWidget(layout),
    );
  }

  static Widget _buildWidget(Map<String, dynamic> node) {
    final type = node["type"]?.toString() ?? "column";
    final props = node["props"] as Map<String, dynamic>? ?? {};

    switch (type) {
      case "column":
        return _buildColumn(node, props);
      case "row":
        return _buildRow(node, props);
      case "topBar":
        return _buildTopBar(node, props);
      default:
        return Container();
    }
  }

  static Widget _buildColumn(Map<String, dynamic> node, Map<String, dynamic> props) {
    final children = node["children"] as List? ?? [];
    return Column(
      children: children.map((child) => _buildWidget(child)).toList(),
    );
  }

  static Widget _buildRow(Map<String, dynamic> node, Map<String, dynamic> props) {
    final children = node["children"] as List? ?? [];
    return Row(
      mainAxisAlignment: _getMainAxisAlignment(props["alignment"]?.toString()),
      children: children.map((child) => _buildWidget(child)).toList(),
    );
  }

  static Widget _buildTopBar(Map<String, dynamic> node, Map<String, dynamic> props) {
    final children = node["children"] as List? ?? [];
    return Container(
      height: (props["height"] ?? 72).toDouble(),
      color: _parseColor(props["background_color"]?.toString() ?? "#080D1F"),
      padding: _getPadding(props["padding"]),
      child: Column(
        children: children.map((child) => _buildWidget(child)).toList(),
      ),
    );
  }

  static MainAxisAlignment _getMainAxisAlignment(String? alignment) {
    switch (alignment) {
      case "spaceBetween":
        return MainAxisAlignment.spaceBetween;
      case "center":
        return MainAxisAlignment.center;
      default:
        return MainAxisAlignment.start;
    }
  }

  static EdgeInsets _getPadding(dynamic padding) {
    if (padding is Map) {
      return EdgeInsets.fromLTRB(
        (padding["left"] ?? 0).toDouble(),
        (padding["top"] ?? 0).toDouble(),
        (padding["right"] ?? 0).toDouble(),
        (padding["bottom"] ?? 0).toDouble(),
      );
    }
    return const EdgeInsets.all(16);
  }
}
