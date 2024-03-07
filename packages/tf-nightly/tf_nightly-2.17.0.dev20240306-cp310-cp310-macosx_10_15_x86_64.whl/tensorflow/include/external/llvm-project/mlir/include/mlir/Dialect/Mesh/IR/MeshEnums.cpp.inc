/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Enum Utility Definitions                                                   *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|* From: MeshOps.td                                                           *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace mesh {
::llvm::StringRef stringifyReductionKind(ReductionKind val) {
  switch (val) {
    case ReductionKind::Sum: return "sum";
    case ReductionKind::Max: return "max";
    case ReductionKind::Min: return "min";
    case ReductionKind::Generic: return "generic";
  }
  return "";
}

::std::optional<ReductionKind> symbolizeReductionKind(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::std::optional<ReductionKind>>(str)
      .Case("sum", ReductionKind::Sum)
      .Case("max", ReductionKind::Max)
      .Case("min", ReductionKind::Min)
      .Case("generic", ReductionKind::Generic)
      .Default(::std::nullopt);
}
::std::optional<ReductionKind> symbolizeReductionKind(uint32_t value) {
  switch (value) {
  case 1: return ReductionKind::Sum;
  case 2: return ReductionKind::Max;
  case 3: return ReductionKind::Min;
  case 100: return ReductionKind::Generic;
  default: return ::std::nullopt;
  }
}

} // namespace mesh
} // namespace mlir

