# from __future__ import annotations

from typing import List, Tuple

import pytermgui as ptg

saldo: float = 0.0
limite: float = 500.0
extrato: List[Tuple[str, float]] = []
numero_saques: int = 0
LIMITE_SAQUES: int = 3


def _configure_widgets() -> None:
    """Define a configuração de todos os widgets globais."""

    ptg.boxes.SINGLE.set_chars_of(ptg.Window)


def _define_layout() -> ptg.Layout:
    """Define o layout da aplicação."""

    layout = ptg.Layout()

    layout.add_slot("header", height=1)
    layout.add_break()

    layout.add_slot("body")
    layout.add_break()

    layout.add_slot("footer", height=1)

    return layout


def _confirm_quit(manager: ptg.WindowManager) -> None:
    """Cria a janela de confirmação de saída."""

    def modal_close(*_: ptg.Button) -> None:
        modal.close(animate=False)

    modal = ptg.Window(
        "[bold]Tem certeza que deseja sair?",
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.KeyboardButton(
                    "Sim", lambda *_: manager.stop(), bound="s"
                ),
                ptg.KeyboardButton(
                    "Não",
                    modal_close,
                    bound="n",
                ),
            ),
        ),
    ).center()

    modal.select(1)
    manager.add(modal, animate=False)


def depositar_(manager: ptg.WindowManager) -> None:
    def modal_close(*_: ptg.Button) -> None:
        modal.close(animate=False)

    def depositar_impl(manager: ptg.WindowManager, input: str) -> None:
        global saldo
        global extrato
        valor = float(input)

        def alert_close(*_: ptg.Button) -> None:
            alert.close(animate=False)

        if valor > 0:
            saldo += valor
            extrato.append((f"Depósito: R$ {valor:.2f}", valor))
            modal_close()
        else:
            alert = (
                ptg.Window(
                    "[bold]A operação de depósito falhou",
                    "",
                    "Tente novamente.",
                    ptg.Container(ptg.Button("OK", alert_close)),
                )
            ).center()
            manager.add(alert, animate=False)

    input_field = ptg.InputField("", multiline=False)
    modal = ptg.Window(
        "[bold]Digite o valor do depósito",
        "",
        ptg.Container(
            ptg.Splitter(
                input_field,
                ptg.Button(
                    "Enter",
                    lambda *_: depositar_impl(manager, input_field.value),
                ),
            ),
        ),
        ptg.Button(
            "Cancelar (Esc)",
            modal_close,
        ),
    ).center()

    modal.bind(ptg.input.keys.ESC, modal_close)
    modal.select(0)
    manager.add(modal, animate=False)


def sacar_(manager: ptg.WindowManager) -> None:
    def modal_close(*_: ptg.Button) -> None:
        modal.close(animate=False)

    def sacar_impl(manager: ptg.WindowManager, input: str) -> None:
        global saldo
        global extrato
        global numero_saques
        global LIMITE_SAQUES
        valor = float(input)

        def alert_close(*_: ptg.Button) -> None:
            alert.close(animate=False)

        valor = float(input)
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

        msg = ""
        if excedeu_saldo:
            msg = "Você não tem saldo suficiente."
        elif excedeu_limite:
            msg = "Operação falhou! O valor do saque excede o limite."
        elif excedeu_saques:
            msg = "Operação falhou! Número máximo de saques excedido."
        elif valor > 0:
            saldo -= valor
            extrato.append((f"Saque:   R$ {valor:.2f}", valor))
            numero_saques += 1
            modal_close()
            return
        else:
            msg = "Operação falhou! O valor informado é inválido."

        alert = (
            ptg.Window(
                "[bold]A operação de saque falhou",
                "",
                f"{msg}",
                ptg.Container(ptg.Button("OK", alert_close)),
            )
        ).center()
        manager.add(alert, animate=False)

    input_field = ptg.InputField("", multiline=False)
    modal = ptg.Window(
        "[bold]Digite o valor que deseja sacar",
        "",
        ptg.Container(
            ptg.Splitter(
                input_field,
                ptg.Button(
                    "Enter",
                    lambda *_: sacar_impl(manager, input_field.value),
                ),
            ),
        ),
        ptg.Button(
            "Cancelar (Esc)",
            modal_close,
        ),
    ).center()

    modal.bind(ptg.input.keys.ESC, modal_close)
    modal.select(0)
    manager.add(modal, animate=False)


def extrato_(manager: ptg.WindowManager) -> None:
    global extrato
    global saldo

    def modal_close(*_: ptg.Button) -> None:
        modal.close(animate=False)

    modal = (
        ptg.Window(
            "[bold]Extrato",
            "",
            "\n".join(map(lambda t: t[0], extrato)),
            f"Saldo: R$ {saldo:.2f}",
            ptg.Container(
                ptg.Button(
                    "Ok",
                    modal_close,
                )
            ),
        ).center()
        if extrato
        else ptg.Window(
            "[bold]A operação de extrato falhou",
            "",
            "Extrato vazio.",
            ptg.Container(
                ptg.Button(
                    "Ok",
                    modal_close,
                )
            ),
        ).center()
    )

    modal.bind(ptg.input.keys.ESC, modal_close)
    modal.select(0)
    manager.add(modal, animate=False)
    pass


def main(argv: list[str] | None = None) -> None:
    """Entrada da aplicação."""

    with ptg.WindowManager() as manager:
        manager.layout = _define_layout()

        header = ptg.Window(
            "Bem Vindo!",
            box="EMPTY",
        )

        manager.add(header, animate=False)

        body = ptg.Window(
            ptg.Container(
                ptg.Container(
                    "Escolha a operação",
                    box=ptg.boxes.Box(["     ", "  x  ", "     "]),
                ),
                ptg.Splitter(
                    ptg.Button(
                        "Depositar",
                        lambda *_: depositar_(manager),
                    ),
                    ptg.Button(
                        "Sacar",
                        lambda *_: sacar_(manager),
                    ),
                    ptg.Button(
                        "Extrato",
                        lambda *_: extrato_(manager),
                    ),
                ),
                static_width=64,
            ),
            box="EMPTY",
        )

        manager.add(body, assign="body", animate=False)

        footer = ptg.Window(
            ptg.Button(
                "Sair (q)",
                lambda *_: _confirm_quit(manager),
            ),
            box="EMPTY",
        )

        manager.add(footer, assign="footer", animate=False)

        manager.bind("q", lambda *_: _confirm_quit(manager))
        manager.focus(body)

    ptg.tim.print("\n[!gradient(210)]Tchau! Até a próxima!")

    # global extrato
    # import pprint as pp
    # pp.pprint(extrato)


if __name__ == "__main__":
    main()
