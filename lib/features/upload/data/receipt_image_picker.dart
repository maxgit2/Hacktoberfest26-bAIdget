import 'dart:typed_data';

import 'package:flutter_image_compress/flutter_image_compress.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';

/// Picks a receipt or payment screenshot from the gallery and prepares it
/// for `POST /expenses/scan`: long side ≤ 2048 px, JPEG quality 85.
class ReceiptImagePicker {
  ReceiptImagePicker({ImagePicker? picker}) : _picker = picker ?? ImagePicker();

  final ImagePicker _picker;

  static const maxSide = 2048.0;
  static const jpegQuality = 85;

  /// JPEG bytes, or null if the user cancels.
  Future<Uint8List?> pick() async {
    // The picker resizes keeping the aspect ratio.
    final picked = await _picker.pickImage(
      source: ImageSource.gallery,
      maxWidth: maxSide,
      maxHeight: maxSide,
      requestFullMetadata: false,
    );
    if (picked == null) return null;

    // Always re-encode to JPEG: handles HEIC/PNG, applies the quality and
    // drops EXIF (e.g. GPS location). The image is already ≤ maxSide, so
    // it is not resized again.
    final jpeg = await FlutterImageCompress.compressWithFile(
      picked.path,
      minWidth: maxSide.toInt(),
      minHeight: maxSide.toInt(),
      quality: jpegQuality,
    );
    if (jpeg == null) throw const FormatException('Could not read the image');
    return jpeg;
  }
}

final receiptImagePickerProvider = Provider<ReceiptImagePicker>(
  (ref) => ReceiptImagePicker(),
);
