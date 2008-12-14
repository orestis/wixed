{	scopeName = 'source.python';
	comment = '
	todo:
		list comprehension / generator comprehension scope.
		
	';
	firstLineMatch = '^#!/.*\bpython\b';
	fileTypes = ( 'py', 'rpy', 'cpy', 'SConstruct', 'Sconstruct', 'sconstruct', 'SConscript' );
	foldingStartMarker = '^\s*(def|class)\s+([.a-zA-Z0-9_ <]+)\s*(\((.*)\))?\s*:|\{\s*$|\(\s*$|\[\s*$|^\s*"""(?=.)(?!.*""")';
	foldingStopMarker = '^\s*$|^\s*\}|^\s*\]|^\s*\)|^\s*"""\s*$';
	patterns = (
		{	name = 'comment.line.number-sign.python';
			match = '(#).*$\n?';
			captures = { 1 = { name = 'punctuation.definition.comment.python'; }; };
		},
		{	name = 'constant.numeric.integer.long.hexadecimal.python';
			match = '\b(?i:(0x\h*)L)';
		},
		{	name = 'constant.numeric.integer.hexadecimal.python';
			match = '\b(?i:(0x\h*))';
		},
		{	name = 'constant.numeric.integer.long.octal.python';
			match = '\b(?i:(0[0-7]+)L)';
		},
		{	name = 'constant.numeric.integer.octal.python';
			match = '\b(0[0-7]+)';
		},
		{	name = 'constant.numeric.complex.python';
			match = '\b(?i:(((\d+(\.(?=[^a-zA-Z_])\d*)?|(?<=[^0-9a-zA-Z_])\.\d+)(e[\-\+]?\d+)?))J)';
		},
		{	name = 'constant.numeric.float.python';
			match = '\b(?i:(\d+\.\d*(e[\-\+]?\d+)?))(?=[^a-zA-Z_])';
		},
		{	name = 'constant.numeric.float.python';
			match = '(?<=[^0-9a-zA-Z_])(?i:(\.\d+(e[\-\+]?\d+)?))';
		},
		{	name = 'constant.numeric.float.python';
			match = '\b(?i:(\d+e[\-\+]?\d+))';
		},
		{	name = 'constant.numeric.integer.long.decimal.python';
			match = '\b(?i:([1-9]+[0-9]*|0)L)';
		},
		{	name = 'constant.numeric.integer.decimal.python';
			match = '\b([1-9]+[0-9]*|0)';
		},
		{	match = '\b(global)\b';
			captures = { 1 = { name = 'storage.modifier.global.python'; }; };
		},
		{	match = '\b(?:(import)|(from))\b';
			captures = {
				1 = { name = 'keyword.control.import.python'; };
				2 = { name = 'keyword.control.import.from.python'; };
			};
		},
		{	name = 'keyword.control.flow.python';
			comment = 'keywords that delimit flow blocks';
			match = '\b(elif|else|except|finally|for|if|try|while|with)\b';
		},
		{	name = 'keyword.control.flow.python';
			comment = 'keywords that alter flow from within a block';
			match = '\b(break|continue|pass|raise|return|yield)\b';
		},
		{	name = 'keyword.operator.logical.python';
			comment = 'keyword operators that evaluate to True or False';
			match = '\b(and|in|is|not|or)\b';
		},
		{	comment = "keywords that haven't fit into other groups (yet).";
			match = '\b(as|assert|del|exec|print)\b';
			captures = { 1 = { name = 'keyword.other.python'; }; };
		},
		{	name = 'keyword.operator.assignment.augmented.python';
			match = '\+\=|-\=|\*\=|/\=|//\=|%\=|&\=|\|\=|\^\=|>>\=|<<\=|\*\*\=';
		},
		{	name = 'keyword.operator.arithmetic.python';
			match = '\+|\-|\*|\*\*|/|//|%|<<|>>|&|\||\^|~';
		},
		{	name = 'keyword.operator.comparison.python';
			match = '<|>|<\=|>\=|\=\=|!\=|<>';
		},
		{	name = 'keyword.operator.assignment.python';
			match = '\=';
		},
		{	name = 'meta.class.old-style.python';
			contentName = 'entity.name.type.class.python';
			begin = '^\s*(class)\s+(?=[a-zA-Z_][a-zA-Z_0-9]*\s*\:)';
			end = '\s*(:)';
			beginCaptures = { 1 = { name = 'storage.type.class.python'; }; };
			endCaptures = { 1 = { name = 'punctuation.section.class.begin.python'; }; };
			patterns = ( { include = '#entity_name_class'; } );
		},
		{	name = 'meta.class.python';
			begin = '^\s*(class)\s+(?=[a-zA-Z_][a-zA-Z_0-9]*\s*\()';
			end = '(\))\s*(?:(\:)|(.*$\n?))';
			beginCaptures = { 1 = { name = 'storage.type.class.python'; }; };
			endCaptures = {
				1 = { name = 'punctuation.definition.inheritance.end.python'; };
				2 = { name = 'punctuation.section.class.begin.python'; };
				3 = { name = 'invalid.illegal.missing-section-begin.python'; };
			};
			patterns = (
				{	contentName = 'entity.name.type.class.python';
					begin = '(?=[A-Za-z_][A-Za-z0-9_]*)';
					end = '(?![A-Za-z0-9_])';
					patterns = ( { include = '#entity_name_class'; } );
				},
				{	contentName = 'meta.class.inheritance.python';
					begin = '(\()';
					end = '(?=\)|:)';
					beginCaptures = { 1 = { name = 'punctuation.definition.inheritance.begin.python'; }; };
					patterns = (
						{	contentName = 'entity.other.inherited-class.python';
							begin = '(?<=\(|,)\s*';
							end = '\s*(?:(,)|(?=\)))';
							endCaptures = { 1 = { name = 'punctuation.separator.inheritance.python'; }; };
							patterns = ( { include = '$self'; } );
						},
					);
				},
			);
		},
		{	name = 'meta.class.python';
			begin = '^\s*(class)\s+(?=[a-zA-Z_][a-zA-Z_0-9])';
			end = '(\()|\s*($\n?|#.*$\n?)';
			beginCaptures = { 1 = { name = 'storage.type.class.python'; }; };
			endCaptures = {
				1 = { name = 'punctuation.definition.inheritance.begin.python'; };
				2 = { name = 'invalid.illegal.missing-inheritance.python'; };
			};
			patterns = (
				{	contentName = 'entity.name.type.class.python';
					begin = '(?=[A-Za-z_][A-Za-z0-9_]*)';
					end = '(?![A-Za-z0-9_])';
					patterns = ( { include = '#entity_name_function'; } );
				},
			);
		},
		{	name = 'meta.function.python';
			begin = '^\s*(def)\s+(?=[A-Za-z_][A-Za-z0-9_]*\s*\()';
			end = '(\))\s*(?:(\:)|(.*$\n?))';
			beginCaptures = { 1 = { name = 'storage.type.function.python'; }; };
			endCaptures = {
				1 = { name = 'punctuation.definition.parameters.end.python'; };
				2 = { name = 'punctuation.section.function.begin.python'; };
				3 = { name = 'invalid.illegal.missing-section-begin.python'; };
			};
			patterns = (
				{	contentName = 'entity.name.function.python';
					begin = '(?=[A-Za-z_][A-Za-z0-9_]*)';
					end = '(?![A-Za-z0-9_])';
					patterns = ( { include = '#entity_name_function'; } );
				},
				{	contentName = 'meta.function.parameters.python';
					begin = '(\()';
					end = '(?=\)\s*\:)';
					beginCaptures = { 1 = { name = 'punctuation.definition.parameters.begin.python'; }; };
					patterns = (
						{	include = '#keyword_arguments'; },
						{	match = '\b([a-zA-Z_][a-zA-Z_0-9]*)\s*(?:(,)|(?=[\n\)]))';
							captures = {
								1 = { name = 'variable.parameter.function.python'; };
								2 = { name = 'punctuation.separator.parameters.python'; };
							};
						},
					);
				},
			);
		},
		{	name = 'meta.function.python';
			begin = '^\s*(def)\s+(?=[A-Za-z_][A-Za-z0-9_]*)';
			end = '(\()|\s*($\n?|#.*$\n?)';
			beginCaptures = { 1 = { name = 'storage.type.function.python'; }; };
			endCaptures = {
				1 = { name = 'punctuation.definition.parameters.begin.python'; };
				2 = { name = 'invalid.illegal.missing-parameters.python'; };
			};
			patterns = (
				{	contentName = 'entity.name.function.python';
					begin = '(?=[A-Za-z_][A-Za-z0-9_]*)';
					end = '(?![A-Za-z0-9_])';
					patterns = ( { include = '#entity_name_function'; } );
				},
			);
		},
		{	name = 'meta.function.decorator.python';
			comment = 'a decorator may be a function call which returns a decorator.';
			begin = '^\s*(?=@\s*[A-Za-z_][A-Za-z0-9_]*(?:\.[a-zA-Z_][a-zA-Z_0-9]*)*\s*\()';
			end = '(\))';
			endCaptures = { 1 = { name = 'punctuation.definition.arguments.end.python'; }; };
			patterns = (
				{	contentName = 'entity.name.function.decorator.python';
					begin = '(?=(@)\s*[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\s*\()';
					end = '(?=\s*\()';
					beginCaptures = { 1 = { name = 'punctuation.definition.decorator.python'; }; };
					patterns = ( { include = '#dotted_name'; } );
				},
				{	contentName = 'meta.function.decorator.arguments.python';
					begin = '(\()';
					end = '(?=\))';
					beginCaptures = { 1 = { name = 'punctuation.definition.arguments.begin.python'; }; };
					patterns = (
						{	include = '#keyword_arguments'; },
						{	include = '$self'; },
					);
				},
			);
		},
		{	name = 'meta.function.decorator.python';
			contentName = 'entity.name.function.decorator.python';
			begin = '^\s*(?=@\s*[A-Za-z_][A-Za-z0-9_]*(?:\.[a-zA-Z_][a-zA-Z_0-9]*)*)';
			end = '(?=\s|$\n?|#)';
			patterns = (
				{	begin = '(?=(@)\s*[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*)';
					end = '(?=\s|$\n?|#)';
					beginCaptures = { 1 = { name = 'punctuation.definition.decorator.python'; }; };
					patterns = ( { include = '#dotted_name'; } );
				},
			);
		},
		{	name = 'meta.function-call.python';
			contentName = 'meta.function-call.arguments.python';
			begin = '(?<=\)|\])\s*(\()';
			end = '(\))';
			beginCaptures = { 1 = { name = 'punctuation.definition.arguments.begin.python'; }; };
			endCaptures = { 1 = { name = 'punctuation.definition.arguments.end.python'; }; };
			patterns = (
				{	include = '#keyword_arguments'; },
				{	include = '$self'; },
			);
		},
		{	name = 'meta.function-call.python';
			begin = '(?=[A-Za-z_][A-Za-z0-9_]*(?:\.[a-zA-Z_][a-zA-Z_0-9]*)*\s*\()';
			end = '(\))';
			endCaptures = { 1 = { name = 'punctuation.definition.arguments.end.python'; }; };
			patterns = (
				{	begin = '(?=[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\s*\()';
					end = '(?=\s*\()';
					patterns = ( { include = '#dotted_name'; } );
				},
				{	contentName = 'meta.function-call.arguments.python';
					begin = '(\()';
					end = '(?=\))';
					beginCaptures = { 1 = { name = 'punctuation.definition.arguments.begin.python'; }; };
					patterns = (
						{	include = '#keyword_arguments'; },
						{	include = '$self'; },
					);
				},
			);
		},
		{	name = 'meta.item-access.python';
			begin = '(?=[A-Za-z_][A-Za-z0-9_]*(?:\.[a-zA-Z_][a-zA-Z_0-9]*)*\s*\[)';
			end = '(\])';
			patterns = (
				{	begin = '(?=[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\s*\[)';
					end = '(?=\s*\[)';
					patterns = ( { include = '#dotted_name'; } );
				},
				{	contentName = 'meta.item-access.arguments.python';
					begin = '(\[)';
					end = '(?=\])';
					beginCaptures = { 1 = { name = 'punctuation.definition.arguments.begin.python'; }; };
					endCaptures = { 1 = { name = 'punctuation.definition.arguments.end.python'; }; };
					patterns = ( { include = '$self'; } );
				},
			);
		},
		{	name = 'meta.item-access.python';
			contentName = 'meta.item-access.arguments.python';
			begin = '(?<=\)|\])\s*(\[)';
			end = '(\])';
			beginCaptures = { 1 = { name = 'punctuation.definition.arguments.begin.python'; }; };
			endCaptures = { 1 = { name = 'punctuation.definition.arguments.end.python'; }; };
			patterns = ( { include = '$self'; } );
		},
		{	match = '\b(def|lambda)\b';
			captures = { 1 = { name = 'storage.type.function.python'; }; };
		},
		{	match = '\b(class)\b';
			captures = { 1 = { name = 'storage.type.class.python'; }; };
		},
		{	include = '#line_continuation'; },
		{	include = '#language_variables'; },
		{	name = 'constant.language.python';
			match = '\b(None|True|False|Ellipsis|NotImplemented)\b';
		},
		{	include = '#string_quoted_single'; },
		{	include = '#string_quoted_double'; },
		{	include = '#dotted_name'; },
		{	begin = '(\()';
			end = '(\))';
			patterns = ( { include = '$self'; } );
		},
		{	match = '(\[)(\s*(\]))\b';
			captures = {
				1 = { name = 'punctuation.definition.list.begin.python'; };
				2 = { name = 'meta.empty-list.python'; };
				3 = { name = 'punctuation.definition.list.end.python'; };
			};
		},
		{	name = 'meta.structure.list.python';
			begin = '(\[)';
			end = '(\])';
			beginCaptures = { 1 = { name = 'punctuation.definition.list.begin.python'; }; };
			endCaptures = { 1 = { name = 'punctuation.definition.list.end.python'; }; };
			patterns = (
				{	contentName = 'meta.structure.list.item.python';
					begin = '(?<=\[|\,)\s*(?![\],])';
					end = '\s*(?:(,)|(?=\]))';
					endCaptures = { 1 = { name = 'punctuation.separator.list.python'; }; };
					patterns = ( { include = '$self'; } );
				},
			);
		},
		{	name = 'meta.structure.tuple.python';
			match = '(\()(\s*(\)))';
			captures = {
				1 = { name = 'punctuation.definition.tuple.begin.python'; };
				2 = { name = 'meta.empty-tuple.python'; };
				3 = { name = 'punctuation.definition.tuple.end.python'; };
			};
		},
		{	name = 'meta.structure.dictionary.python';
			match = '(\{)(\s*(\}))';
			captures = {
				1 = { name = 'punctuation.definition.dictionary.begin.python'; };
				2 = { name = 'meta.empty-dictionary.python'; };
				3 = { name = 'punctuation.definition.dictionary.end.python'; };
			};
		},
		{	name = 'meta.structure.dictionary.python';
			begin = '(\{)';
			end = '(\})';
			beginCaptures = { 1 = { name = 'punctuation.definition.dictionary.begin.python'; }; };
			endCaptures = { 1 = { name = 'punctuation.definition.dictionary.end.python'; }; };
			patterns = (
				{	contentName = 'meta.structure.dictionary.key.python';
					begin = '(?<=\{|\,|^)\s*(?![\},])';
					end = '\s*(?:(?=\})|(\:))';
					endCaptures = { 1 = { name = 'punctuation.separator.valuepair.dictionary.python'; }; };
					patterns = ( { include = '$self'; } );
				},
				{	contentName = 'meta.structure.dictionary.value.python';
					begin = '(?<=\:|^)\s*';
					end = '\s*(?:(?=\})|(,))';
					endCaptures = { 1 = { name = 'punctuation.separator.dictionary.python'; }; };
					patterns = ( { include = '$self'; } );
				},
			);
		},
	);
	repository = {
		builtin_exceptions = {
			name = 'support.type.exception.python';
			match = '(?x)\b((Arithmetic|Assertion|Attribute|EOF|Environment|FloatingPoint|IO|Import|Indentation|Index|Key|Lookup|Memory|Name|OS|Overflow|NotImplemented|Reference|Runtime|Standard|Syntax|System|Tab|Type|UnboundLocal|Unicode(Translate|Encode|Decode)?|Value|ZeroDivision)Error|(Deprecation|Future|Overflow|PendingDeprecation|Runtime|Syntax|User)?Warning|KeyboardInterrupt|NotImplemented|StopIteration|SystemExit|(Base)?Exception)\b';
		};
		builtin_functions = {
			name = 'support.function.builtin.python';
			match = '(?x)\b(
                __import__|all|abs|any|apply|callable|chr|cmp|coerce|compile|delattr|dir|
                divmod|eval|execfile|filter|getattr|globals|hasattr|hash|hex|id|
                input|intern|isinstance|issubclass|iter|len|locals|map|max|min|oct|
                ord|pow|range|raw_input|reduce|reload|repr|round|setattr|sorted|
                sum|unichr|vars|zip
			)\b';
		};
		builtin_types = {
			name = 'support.type.python';
			match = '(?x)\b(
				basestring|bool|buffer|classmethod|complex|dict|enumerate|file|
				float|frozenset|int|list|long|object|open|property|reversed|set|
				slice|staticmethod|str|super|tuple|type|unicode|xrange
			)\b';
		};
		constant_placeholder = {
			name = 'constant.other.placeholder.python';
			match = '(?i:%(\([a-z_]+\))?#?0?\-?[ ]?\+?([0-9]*|\*)(\.([0-9]*|\*))?[hL]?[a-z%])';
		};
		docstrings = {
			patterns = (
				{	name = 'comment.block.python';
					begin = '^\s*(?=[uU]?[rR]?""")';
					end = '(?<=""")';
					patterns = ( { include = '#string_quoted_double'; } );
				},
				{	name = 'comment.block.python';
					begin = "^\s*(?=[uU]?[rR]?''')";
					end = "(?<=''')";
					patterns = ( { include = '#string_quoted_single'; } );
				},
			);
		};
		dotted_name = {
			begin = '(?=[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)';
			end = '(?![A-Za-z0-9_\.])';
			patterns = (
				{	begin = '(\.)(?=[A-Za-z_][A-Za-z0-9_]*)';
					end = '(?![A-Za-z0-9_])';
					patterns = (
						{	include = '#magic_function_names'; },
						{	include = '#magic_variable_names'; },
						{	include = '#illegal_names'; },
						{	include = '#generic_names'; },
					);
				},
				{	begin = '(?<!\.)(?=[A-Za-z_][A-Za-z0-9_]*)';
					end = '(?![A-Za-z0-9_])';
					patterns = (
						{	include = '#builtin_functions'; },
						{	include = '#builtin_types'; },
						{	include = '#builtin_exceptions'; },
						{	include = '#illegal_names'; },
						{	include = '#magic_function_names'; },
						{	include = '#magic_variable_names'; },
						{	include = '#language_variables'; },
						{	include = '#generic_names'; },
					);
				},
			);
		};
		entity_name_class = {
			patterns = (
				{	include = '#illegal_names'; },
				{	include = '#generic_names'; },
			);
		};
		entity_name_function = {
			patterns = (
				{	include = '#magic_function_names'; },
				{	include = '#illegal_names'; },
				{	include = '#generic_names'; },
			);
		};
		escaped_char = {
			match = '(\\x[0-9A-F]{2})|(\\[0-7]{3})|(\\\n)|(\\\\)|(\\\")|(\\'')|(\\a)|(\\b)|(\\f)|(\\n)|(\\r)|(\\t)|(\\v)';
			captures = {
				1 = { name = 'constant.character.escape.hex.python'; };
				2 = { name = 'constant.character.escape.octal.python'; };
				3 = { name = 'constant.character.escape.newline.python'; };
				4 = { name = 'constant.character.escape.backlash.python'; };
				5 = { name = 'constant.character.escape.double-quote.python'; };
				6 = { name = 'constant.character.escape.single-quote.python'; };
				7 = { name = 'constant.character.escape.bell.python'; };
				8 = { name = 'constant.character.escape.backspace.python'; };
				9 = { name = 'constant.character.escape.formfeed.python'; };
				10 = { name = 'constant.character.escape.linefeed.python'; };
				11 = { name = 'constant.character.escape.return.python'; };
				12 = { name = 'constant.character.escape.tab.python'; };
				13 = { name = 'constant.character.escape.vertical-tab.python'; };
			};
		};
		escaped_unicode_char = {
			match = '(\\U[0-9A-Fa-f]{8})|(\\u[0-9A-Fa-f]{4})|(\\N\{[a-zA-Z ]+\})';
			captures = {
				1 = { name = 'constant.character.escape.unicode.16-bit-hex.python'; };
				2 = { name = 'constant.character.escape.unicode.32-bit-hex.python'; };
				3 = { name = 'constant.character.escape.unicode.name.python'; };
			};
		};
		function_name = {
			patterns = (
				{	include = '#magic_function_names'; },
				{	include = '#magic_variable_names'; },
				{	include = '#builtin_exceptions'; },
				{	include = '#builtin_functions'; },
				{	include = '#builtin_types'; },
				{	include = '#generic_names'; },
			);
		};
		generic_names = { match = '[A-Za-z_][A-Za-z0-9_]*'; };
		illegal_names = {
			name = 'invalid.illegal.name.python';
			match = '\b(and|as|assert|break|class|continue|def|del|elif|else|except|exec|finally|for|from|global|if|import|in|is|lambda|not|or|pass|print|raise|return|try|while|with|yield)\b';
		};
		keyword_arguments = {
			begin = '\b([a-zA-Z_][a-zA-Z_0-9]*)\s*(=)(?!=)';
			end = '\s*(?:(,)|(?=$\n?|[\)]))';
			beginCaptures = {
				1 = { name = 'variable.parameter.function.python'; };
				2 = { name = 'keyword.operator.assignment.python'; };
			};
			endCaptures = { 1 = { name = 'punctuation.separator.parameters.python'; }; };
			patterns = ( { include = '$self'; } );
		};
		language_variables = {
			name = 'variable.language.python';
			match = '\b(self|cls)\b';
		};
		line_continuation = {
			match = '(\\)(.*)$\n?';
			captures = {
				1 = { name = 'punctuation.separator.continuation.line.python'; };
				2 = { name = 'invalid.illegal.unexpected-text.python'; };
			};
		};
		magic_function_names = {
			name = 'support.function.magic.python';
			comment = 'these methods have magic interpretation by python and are generally called indirectly through syntactic constructs';
			match = '(?x)\b(__(?:
						abs|add|and|call|cmp|coerce|complex|contains|del|delattr|
						delete|delitem|delslice|div|divmod|enter|eq|exit|float|
						floordiv|ge|get|getattr|getattribute|getitem|getslice|gt|
						hash|hex|iadd|iand|idiv|ifloordiv|ilshift|imod|imul|init|
						int|invert|ior|ipow|irshift|isub|iter|itruediv|ixor|le|len|
						long|lshift|lt|mod|mul|ne|neg|new|nonzero|oct|or|pos|pow|
						radd|rand|rdiv|rdivmod|repr|rfloordiv|rlshift|rmod|rmul|ror|
						rpow|rrshift|rshift|rsub|rtruediv|rxor|set|setattr|setitem|
						setslice|str|sub|truediv|unicode|xor
					)__)\b';
		};
		magic_variable_names = {
			name = 'support.variable.magic.python';
			comment = 'magic variables which a class/module may have.';
			match = '\b__(all|bases|class|debug|dict|doc|file|members|metaclass|methods|name|slots|weakref)__\b';
		};
		regular_expressions = {
			comment = 'Changed disabled to 1 to turn off syntax highlighting in “r” strings.';
			patterns = ( { include = 'source.regexp.python'; } );
			disabled = 0;
		};
		string_quoted_double = {
			patterns = (
				{	name = 'string.quoted.double.block.unicode-raw-regex.python';
					comment = 'single quoted unicode-raw string';
					begin = '([uU]r)(""")';
					end = '((?<=""")(")""|""")';
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.double.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_unicode_char'; },
						{	include = '#escaped_char'; },
						{	include = '#regular_expressions'; },
					);
				},
				{	name = 'string.quoted.double.block.unicode-raw.python';
					comment = 'single quoted unicode-raw string without regular expression highlighting';
					begin = '([uU]R)(""")';
					end = '((?<=""")(")""|""")';
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.double.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_unicode_char'; },
						{	include = '#escaped_char'; },
					);
				},
				{	name = 'string.quoted.double.block.raw-regex.python';
					comment = 'double quoted raw string';
					begin = '(r)(""")';
					end = '((?<=""")(")""|""")';
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.double.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
						{	include = '#regular_expressions'; },
					);
				},
				{	name = 'string.quoted.double.block.raw.python';
					comment = 'double quoted raw string';
					begin = '(R)(""")';
					end = '((?<=""")(")""|""")';
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.double.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
					);
				},
				{	name = 'string.quoted.double.block.unicode.python';
					comment = 'double quoted unicode string';
					begin = '([uU])(""")';
					end = '((?<=""")(")""|""")';
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.double.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_unicode_char'; },
						{	include = '#escaped_char'; },
					);
				},
				{	name = 'string.quoted.double.single-line.unicode-raw-regex.python';
					comment = 'double-quoted raw string';
					begin = '([uU]r)(")';
					end = '((?<=")(")|")|(\n)';
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.double.python'; };
						3 = { name = 'invalid.illegal.unclosed-string.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_unicode_char'; },
						{	include = '#escaped_char'; },
						{	include = '#regular_expressions'; },
					);
				},
				{	name = 'string.quoted.double.single-line.unicode-raw.python';
					comment = 'double-quoted raw string';
					begin = '([uU]R)(")';
					end = '((?<=")(")|")|(\n)';
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.double.python'; };
						3 = { name = 'invalid.illegal.unclosed-string.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_unicode_char'; },
						{	include = '#escaped_char'; },
					);
				},
				{	name = 'string.quoted.double.single-line.raw-regex.python';
					comment = 'double-quoted raw string';
					begin = '(r)(")';
					end = '((?<=")(")|")|(\n)';
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.double.python'; };
						3 = { name = 'invalid.illegal.unclosed-string.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
						{	include = '#regular_expressions'; },
					);
				},
				{	name = 'string.quoted.double.single-line.raw.python';
					comment = 'double-quoted raw string';
					begin = '(R)(")';
					end = '((?<=")(")|")|(\n)';
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.double.python'; };
						3 = { name = 'invalid.illegal.unclosed-string.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
					);
				},
				{	name = 'string.quoted.double.single-line.unicode.python';
					comment = 'double quoted unicode string';
					begin = '([uU])(")';
					end = '((?<=")(")|")|(\n)';
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.double.python'; };
						3 = { name = 'invalid.illegal.unclosed-string.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_unicode_char'; },
						{	include = '#escaped_char'; },
					);
				},
				{	name = 'string.quoted.double.block.sql.python';
					comment = 'double quoted string';
					begin = '(""")(?=\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|REPLACE|ALTER))';
					end = '((?<=""")(")""|""")';
					beginCaptures = { 1 = { name = 'punctuation.definition.string.begin.python'; }; };
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.double.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
						{	include = 'source.sql'; },
					);
				},
				{	name = 'string.quoted.double.single-line.sql.python';
					comment = 'double quoted string';
					begin = '(")(?=\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|REPLACE|ALTER))';
					end = '((?<=")(")|")|(\n)';
					beginCaptures = { 1 = { name = 'punctuation.definition.string.begin.python'; }; };
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.double.python'; };
						3 = { name = 'invalid.illegal.unclosed-string.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
						{	include = 'source.sql'; },
					);
				},
				{	name = 'string.quoted.double.block.python';
					comment = 'double quoted string';
					begin = '(""")';
					end = '((?<=""")(")""|""")';
					beginCaptures = { 1 = { name = 'punctuation.definition.string.begin.python'; }; };
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.double.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
					);
				},
				{	name = 'string.quoted.double.single-line.python';
					comment = 'double quoted string';
					begin = '(")';
					end = '((?<=")(")|")|(\n)';
					beginCaptures = { 1 = { name = 'punctuation.definition.string.begin.python'; }; };
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.double.python'; };
						3 = { name = 'invalid.illegal.unclosed-string.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
					);
				},
			);
		};
		string_quoted_single = {
			patterns = (
				{	name = 'string.quoted.single.single-line.python';
					match = "(?<!')(')(('))(?!')";
					captures = {
						1 = { name = 'punctuation.definition.string.begin.python'; };
						2 = { name = 'punctuation.definition.string.end.python'; };
						3 = { name = 'meta.empty-string.single.python'; };
					};
				},
				{	name = 'string.quoted.single.block.unicode-raw-regex.python';
					comment = 'single quoted unicode-raw string';
					begin = "([uU]r)(''')";
					end = "((?<=''')(')''|''')";
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.single.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_unicode_char'; },
						{	include = '#escaped_char'; },
						{	include = '#regular_expressions'; },
					);
				},
				{	name = 'string.quoted.single.block.unicode-raw.python';
					comment = 'single quoted unicode-raw string';
					begin = "([uU]R)(''')";
					end = "((?<=''')(')''|''')";
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.single.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_unicode_char'; },
						{	include = '#escaped_char'; },
					);
				},
				{	name = 'string.quoted.single.block.raw-regex.python';
					comment = 'single quoted raw string';
					begin = "(r)(''')";
					end = "((?<=''')(')''|''')";
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.single.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
						{	include = '#regular_expressions'; },
					);
				},
				{	name = 'string.quoted.single.block.raw.python';
					comment = 'single quoted raw string';
					begin = "(R)(''')";
					end = "((?<=''')(')''|''')";
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.single.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
					);
				},
				{	name = 'string.quoted.single.block.unicode.python';
					comment = 'single quoted unicode string';
					begin = "([uU])(''')";
					end = "((?<=''')(')''|''')";
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.single.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_unicode_char'; },
						{	include = '#escaped_char'; },
					);
				},
				{	name = 'string.quoted.single.single-line.unicode-raw-regex.python';
					comment = 'single quoted raw string';
					begin = "([uU]r)(')";
					end = "(')|(\n)";
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'invalid.illegal.unclosed-string.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_unicode_char'; },
						{	include = '#escaped_char'; },
						{	include = '#regular_expressions'; },
					);
				},
				{	name = 'string.quoted.single.single-line.unicode-raw.python';
					comment = 'single quoted raw string';
					begin = "([uU]R)(')";
					end = "(')|(\n)";
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'invalid.illegal.unclosed-string.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_unicode_char'; },
						{	include = '#escaped_char'; },
					);
				},
				{	name = 'string.quoted.single.single-line.raw-regex.python';
					comment = 'single quoted raw string';
					begin = "(r)(')";
					end = "(')|(\n)";
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'invalid.illegal.unclosed-string.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
						{	include = '#regular_expressions'; },
					);
				},
				{	name = 'string.quoted.single.single-line.raw.python';
					comment = 'single quoted raw string';
					begin = "(R)(')";
					end = "(')|(\n)";
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'invalid.illegal.unclosed-string.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
					);
				},
				{	name = 'string.quoted.single.single-line.unicode.python';
					comment = 'single quoted unicode string';
					begin = "([uU])(')";
					end = "(')|(\n)";
					beginCaptures = {
						1 = { name = 'storage.type.string.python'; };
						2 = { name = 'punctuation.definition.string.begin.python'; };
					};
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'invalid.illegal.unclosed-string.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_unicode_char'; },
						{	include = '#escaped_char'; },
					);
				},
				{	name = 'string.quoted.single.block.python';
					comment = 'single quoted string';
					begin = "(''')(?=\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|REPLACE|ALTER))";
					end = "((?<=''')(')''|''')";
					beginCaptures = { 1 = { name = 'punctuation.definition.string.begin.python'; }; };
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.single.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
						{	include = 'source.sql'; },
					);
				},
				{	name = 'string.quoted.single.single-line.python';
					comment = 'single quoted string';
					begin = "(')(?=\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|REPLACE|ALTER))";
					end = "(')|(\n)";
					beginCaptures = { 1 = { name = 'punctuation.definition.string.begin.python'; }; };
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'invalid.illegal.unclosed-string.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
						{	include = 'source.sql'; },
					);
				},
				{	name = 'string.quoted.single.block.python';
					comment = 'single quoted string';
					begin = "(''')";
					end = "((?<=''')(')''|''')";
					beginCaptures = { 1 = { name = 'punctuation.definition.string.begin.python'; }; };
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'meta.empty-string.single.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
					);
				},
				{	name = 'string.quoted.single.single-line.python';
					comment = 'single quoted string';
					begin = "(')";
					end = "(')|(\n)";
					beginCaptures = { 1 = { name = 'punctuation.definition.string.begin.python'; }; };
					endCaptures = {
						1 = { name = 'punctuation.definition.string.end.python'; };
						2 = { name = 'invalid.illegal.unclosed-string.python'; };
					};
					patterns = (
						{	include = '#constant_placeholder'; },
						{	include = '#escaped_char'; },
					);
				},
			);
		};
		strings = {
			patterns = (
				{	include = '#string_quoted_double'; },
				{	include = '#string_quoted_single'; },
			);
		};
	};
}

